from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import random

from auth.auth_utils import get_db, get_current_user
from models.database import Name, User, Vote
from schemas.schemas import NameResponse, NameCreate, NameInfoResponse
from utils.wikionary_fetcher import extract_name_info
from utils.error_utils import handle_error, log_info, log_warning

router = APIRouter()


# GET /names/random?n=10&gender=m&exclude_voted=true
@router.get("/random", response_model=List[NameResponse])
def get_random_names(
    n: int = Query(1, ge=1, le=100),
    gender: Optional[str] = None,
    exclude_voted: bool = Query(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get up to n weighted random names the user hasn't voted on yet."""
    log_info(
        f"Requesting {n} random names, gender={gender}, user={current_user.username}",
        "get_random_names",
    )

    # Base query
    query = db.query(Name)

    # Exclude names the user has voted on if exclude_voted is True
    if exclude_voted:
        voted_subq = db.query(Vote.name_id).filter(Vote.user_id == current_user.id)
        query = query.filter(~Name.id.in_(voted_subq))

    # Apply gender filter if valid
    if gender and gender.lower() in {"m", "f"}:
        query = query.filter(Name.gender == gender.lower())

    # Pull all eligible names into memory (OK up to ~10k rows)
    eligible_names = query.all()

    if not eligible_names:
        log_warning("No names available for user to vote on", "get_random_names")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

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
