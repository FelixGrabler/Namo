from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from auth.auth_utils import get_db, get_current_user
from models.database import Vote, User, Name
from schemas.schemas import VoteCreate, VoteResponse, VoteWithName

router = APIRouter()


# POST /votes/
@router.post("/", response_model=VoteResponse)
def create_or_update_vote(
    vote: VoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create or update a vote for a name."""
    name = db.query(Name).filter(Name.id == vote.name_id).first()
    if not name:
        raise HTTPException(status_code=404, detail="Name not found")

    existing = (
        db.query(Vote)
        .filter(Vote.user_id == current_user.id, Vote.name_id == vote.name_id)
        .first()
    )

    if existing:
        existing.vote = vote.vote
        db.commit()
        db.refresh(existing)
        return existing
    else:
        new_vote = Vote(user_id=current_user.id, name_id=vote.name_id, vote=vote.vote)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return new_vote


# GET /votes?vote=true&skip=0&limit=100
@router.get("/", response_model=List[VoteWithName])
def get_votes(
    vote: Optional[bool] = Query(None),
    skip: int = 0,
    limit: int = Query(100, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get current user's votes, optionally filtered by vote type."""
    query = (
        db.query(Vote)
        .filter(Vote.user_id == current_user.id)
        .options(joinedload(Vote.name))
        .join(Name)
        .order_by(Name.name.asc())  # Order alphabetically by name
    )

    if vote is not None:
        query = query.filter(Vote.vote == vote)

    return query.offset(skip).limit(limit).all()


# DELETE /votes/by-name/{name_id}
@router.delete("/by-name/{name_id}")
def delete_vote_by_name(
    name_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a vote by name ID for the current user."""
    vote = (
        db.query(Vote)
        .filter(Vote.user_id == current_user.id, Vote.name_id == name_id)
        .first()
    )

    if not vote:
        raise HTTPException(status_code=404, detail="Vote not found")

    db.delete(vote)
    db.commit()
    return {"message": "Vote deleted successfully"}


# GET /votes/compare?other_username=jessica
@router.get("/compare", response_model=dict)
def compare_votes(
    other_username: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Compare mutual and unique likes between current user and another user."""
    other_user = db.query(User).filter(User.username == other_username).first()
    if not other_user:
        raise HTTPException(status_code=404, detail="Other user not found")

    # Fetch liked names for both users
    user_votes = (
        db.query(Vote)
        .filter(Vote.user_id == current_user.id, Vote.vote.is_(True))
        .options(joinedload(Vote.name))
        .all()
    )

    other_votes = (
        db.query(Vote)
        .filter(Vote.user_id == other_user.id, Vote.vote.is_(True))
        .options(joinedload(Vote.name))
        .all()
    )

    user_name_ids = {v.name_id: v.name for v in user_votes}
    other_name_ids = {v.name_id: v.name for v in other_votes}

    both = []
    only_you = []
    only_other = []

    for name_id in user_name_ids:
        if name_id in other_name_ids:
            both.append(user_name_ids[name_id])
        else:
            only_you.append(user_name_ids[name_id])

    for name_id in other_name_ids:
        if name_id not in user_name_ids:
            only_other.append(other_name_ids[name_id])

    return {
        "both": both,
        "only_you": only_you,
        "only_other": only_other,
    }
