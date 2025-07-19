from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from auth.auth_utils import get_db, get_current_user
from models.database import Name, User
from schemas.schemas import NameResponse, NameCreate

router = APIRouter()


@router.get("/random", response_model=NameResponse)
def get_random_name(
    gender: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a random name, optionally filtered by gender."""
    query = db.query(Name)

    # Filter by gender if provided
    if gender and gender.lower() in ["m", "f"]:
        query = query.filter(Name.gender == gender.lower())

    # Get random name
    name = query.order_by(func.random()).first()

    if not name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No names found"
        )

    return name


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
