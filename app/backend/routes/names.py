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


@router.get("/random", response_model=List[NameResponse])
def get_random_names(
    n: int = Query(1, ge=1, le=100),
    gender: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get up to n weighted random names the user hasn't voted on yet."""
    log_info(
        f"Requesting {n} random names, gender={gender}, user={current_user.username}",
        "get_random_names",
    )

    # Get name IDs the user has already voted on
    voted_subq = db.query(Vote.name_id).filter(Vote.user_id == current_user.id)

    # Base query
    query = db.query(Name).filter(
        ~Name.id.in_(voted_subq), Name.count > 0  # ensure weights are valid
    )

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


@router.get("/", response_model=List[NameResponse])
def get_names(
    skip: int = 0,
    limit: int = 100,
    gender: Optional[str] = None,
    source: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get list of names with optional filters."""
    query = db.query(Name)

    # Apply filters
    if gender and gender.lower() in ["m", "f"]:
        query = query.filter(Name.gender == gender.lower())

    if source:
        query = query.filter(Name.source.ilike(f"%{source}%"))

    names = query.offset(skip).limit(limit).all()
    return names


@router.post("/", response_model=NameResponse)
def create_name(
    name: NameCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new name entry."""
    db_name = Name(**name.dict())
    db.add(db_name)
    db.commit()
    db.refresh(db_name)
    return db_name


@router.get("/{name_id}", response_model=NameResponse)
def get_name(
    name_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific name by ID."""
    name = db.query(Name).filter(Name.id == name_id).first()
    if not name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Name not found"
        )
    return name


@router.get("/info/{name}", response_model=NameInfoResponse)
def get_name_info(
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get detailed information about a name."""
    name_entry = db.query(Name).filter(Name.name == name).first()
    if not name_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Name not found"
        )

    # Get additional info from Wiktionary
    wiktionary_info = extract_name_info(name)

    if not wiktionary_info:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Name information not available from Wiktionary",
        )

    return NameInfoResponse(
        id=name_entry.id,
        name=name_entry.name,
        info=wiktionary_info,
    )
