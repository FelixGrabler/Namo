from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from auth.auth_utils import get_db, get_current_user
from models.database import Vote, User, Name
from schemas.schemas import VoteCreate, VoteResponse, VoteWithName

router = APIRouter()


@router.post("/", response_model=VoteResponse)
def create_vote(
    vote: VoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create or update a vote for a name."""
    # Check if name exists
    name = db.query(Name).filter(Name.id == vote.name_id).first()
    if not name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Name not found"
        )

    # Check if vote already exists
    existing_vote = (
        db.query(Vote)
        .filter(Vote.user_id == current_user.id, Vote.name_id == vote.name_id)
        .first()
    )

    if existing_vote:
        # Update existing vote
        existing_vote.vote = vote.vote
        db.commit()
        db.refresh(existing_vote)
        return existing_vote
    else:
        # Create new vote
        db_vote = Vote(user_id=current_user.id, name_id=vote.name_id, vote=vote.vote)
        try:
            db.add(db_vote)
            db.commit()
            db.refresh(db_vote)
            return db_vote
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vote could not be created",
            )


@router.get("/my-votes", response_model=List[VoteWithName])
def get_my_votes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get current user's votes."""
    votes = (
        db.query(Vote)
        .filter(Vote.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return votes


@router.delete("/{vote_id}")
def delete_vote(
    vote_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a vote."""
    vote = (
        db.query(Vote)
        .filter(Vote.id == vote_id, Vote.user_id == current_user.id)
        .first()
    )

    if not vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found"
        )

    db.delete(vote)
    db.commit()
    return {"message": "Vote deleted successfully"}


@router.get("/{name_id}/stats")
def get_vote_stats(
    name_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get voting statistics for a name."""
    # Check if name exists
    name = db.query(Name).filter(Name.id == name_id).first()
    if not name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Name not found"
        )

    # Count likes and dislikes
    total_votes = db.query(Vote).filter(Vote.name_id == name_id).count()
    likes = db.query(Vote).filter(Vote.name_id == name_id, Vote.vote == True).count()
    dislikes = total_votes - likes

    return {
        "name_id": name_id,
        "name": name.name,
        "total_votes": total_votes,
        "likes": likes,
        "dislikes": dislikes,
        "like_percentage": round(
            (likes / total_votes * 100) if total_votes > 0 else 0, 2
        ),
    }
