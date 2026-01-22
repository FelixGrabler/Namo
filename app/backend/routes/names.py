from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import random
import re

from auth.auth_utils import get_db, get_current_user
from models.database import Name, User, Vote
from schemas.schemas import NameResponse, NameCreate, NameInfoResponse
from utils.wikionary_fetcher import extract_name_info
from utils.error_utils import handle_error, log_info, log_warning

router = APIRouter()


# GET /names/random?n=10&genders=male,female&sort_order=random&exclude_voted=true
@router.get("/random", response_model=List[NameResponse])
def get_random_names(
    n: int = Query(1, ge=1, le=100),
    genders: Optional[str] = None,
    sort_order: Optional[str] = Query("random"),
    exclude_voted: bool = Query(True),
    source: Optional[str] = None,
    require_count: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get up to n weighted random names the user hasn't voted on yet."""
    log_info(
        f"Requesting {n} random names, genders={genders}, sort_order={sort_order}, user={current_user.username}",
        "get_random_names",
    )

    # Base query
    query = db.query(Name)

    # Exclude names the user has voted on if exclude_voted is True
    if exclude_voted:
        voted_subq = db.query(Vote.name_id).filter(Vote.user_id == current_user.id)
        query = query.filter(~Name.id.in_(voted_subq))

    if source:
        query = query.filter(Name.source.ilike(f"%{source}%"))

    # Apply gender filter if valid
    if genders:
        gender_list = [g.strip().lower() for g in genders.split(",")]
        # Convert frontend gender names to database format
        db_genders = []
        for gender in gender_list:
            if gender == "male":
                db_genders.append("m")
            elif gender == "female":
                db_genders.append("f")

        if db_genders:
            query = query.filter(Name.gender.in_(db_genders))

    if require_count:
        query = query.filter(Name.count.isnot(None))

    # Pull all eligible names into memory (OK up to ~10k rows)
    eligible_names = query.all()

    if not eligible_names:
        log_warning("No names available for user to vote on", "get_random_names")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    # Apply sorting based on sort_order
    if sort_order == "most_popular":
        eligible_names.sort(key=lambda name: name.count, reverse=True)
        selected = eligible_names[:n]
    elif sort_order == "least_popular":
        eligible_names.sort(key=lambda name: name.count)
        selected = eligible_names[:n]
    else:  # random (default)
        if len(eligible_names) <= n:
            selected = eligible_names
        else:
            # Sample without replacement using weights
            weights = [name.count for name in eligible_names]
            selected = random.choices(
                population=eligible_names,
                weights=weights,
                k=n * 2,  # oversample to avoid dupes
            )

            # Remove duplicates and trim to `n`
            seen = set()
            unique_selected = []
            for name in selected:
                if name.id not in seen:
                    unique_selected.append(name)
                    seen.add(name.id)
                if len(unique_selected) == n:
                    break
            selected = unique_selected

    log_info(f"Returning {len(selected)} random names", "get_random_names")
    return selected


# GET /names/search?q=anna&limit=20&after_name=anna&after_id=10&source=austria
@router.get("/search", response_model=List[NameResponse])
def search_names(
    q: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    after_name: Optional[str] = None,
    after_id: Optional[int] = None,
    source: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search names by substring with simple keyset pagination."""
    query = db.query(Name)

    if q:
        query = query.filter(Name.name.ilike(f"%{q}%"))

    if source:
        query = query.filter(Name.source.ilike(f"%{source}%"))

    if after_name:
        if after_id is None:
            raise HTTPException(status_code=400, detail="after_id required with after_name")
        after_name_lower = after_name.lower()
        query = query.filter(
            (func.lower(Name.name) > after_name_lower)
            | ((func.lower(Name.name) == after_name_lower) & (Name.id > after_id))
        )

    query = query.order_by(func.lower(Name.name).asc(), Name.id.asc())
    return query.limit(limit).all()


# GET /names/ordered?direction=popular&after=123&limit=10&source=source_name&gender=m
@router.get("/ordered", response_model=List[NameResponse])
def get_ordered_names(
    direction: str = Query("popular", regex="^(popular|unpopular)$"),
    after: Optional[int] = None,  # name_id
    limit: int = Query(1, ge=1, le=100),
    source: Optional[str] = None,
    gender: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return names ordered by count (popular/unpopular), filtered by source/gender,
    excluding names already voted on by the user.
    Supports keyset pagination via `after` (name.id).
    """

    # Validate direction
    asc = direction == "unpopular"

    # Base query: exclude already voted names
    voted_subq = db.query(Vote.name_id).filter(Vote.user_id == current_user.id)
    query = db.query(Name).filter(~Name.id.in_(voted_subq))

    # Apply filters
    if source:
        query = query.filter(Name.source.ilike(f"%{source}%"))

    if gender and gender.lower() in ["m", "f"]:
        query = query.filter(Name.gender == gender.lower())

    # If `after` is given, use keyset pagination
    if after:
        anchor = db.query(Name).filter(Name.id == after).first()
        if not anchor:
            raise HTTPException(status_code=400, detail="Invalid `after` value")

        anchor_count = anchor.count
        anchor_id = anchor.id

        if asc:
            query = query.filter(
                (Name.count > anchor_count)
                | ((Name.count == anchor_count) & (Name.id > anchor_id))
            )
        else:
            query = query.filter(
                (Name.count < anchor_count)
                | ((Name.count == anchor_count) & (Name.id > anchor_id))
            )

    # Apply ordering
    if asc:
        query = query.order_by(Name.count.asc(), Name.id.asc())
    else:
        query = query.order_by(Name.count.desc(), Name.id.asc())

    # Limit results
    results = query.limit(limit).all()

    if not results:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    return results


# GET /names/info/{name}
@router.get("/info/{name}", response_model=NameInfoResponse)
def get_name_info(
    name: str,
):
    """Get detailed information about a name."""
    wiktionary_info = extract_name_info(name)

    if not wiktionary_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Name information not available from Wiktionary",
        )

    return NameInfoResponse(
        name=name,
        info=wiktionary_info,
    )


# GET /names/wordle/random
@router.get("/wordle/random", response_model=dict)
def get_random_wordle_name(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return a random 5-letter A-Za-z name for Wordle."""
    eligible = (
        db.query(Name.name)
        .filter(
            func.length(Name.name) == 5,
            Name.name.op("~")("^[A-Za-z]{5}$"),
        )
        .all()
    )

    if not eligible:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    selected = random.choice(eligible)[0]
    return {"name": selected}


# GET /names/wordle/validate?name=Annaa
@router.get("/wordle/validate", response_model=dict)
def validate_wordle_name(
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Validate a Wordle guess against available 5-letter names."""
    if not re.match(r"^[A-Za-z]{5}$", name):
        return {"valid": False}

    exists = (
        db.query(Name.id)
        .filter(
            func.length(Name.name) == 5,
            func.lower(Name.name) == name.lower(),
            Name.name.op("~")("^[A-Za-z]{5}$"),
        )
        .first()
        is not None
    )
    return {"valid": exists}
