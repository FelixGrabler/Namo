from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List

from auth.auth_utils import (
    get_db,
    get_current_user,
    request_auth_token,
)
from models.database import User
from schemas.schemas import UserCreate, UserResponse, UserLogin, Token
from utils.logging_config import APP_LOGGER

router = APIRouter()


@router.post("/register", response_model=Token)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register via shared auth and sync the local Namo user mirror."""

    APP_LOGGER.info(f"Registration attempt for user: {user.username}")

    try:
        token_payload = request_auth_token(user.username, user.password, "register")
        db_user = get_current_user(
            token_data={
                "username": user.username,
                "auth_user_id": _decode_token_user_id(token_payload["access_token"]),
                "token": token_payload["access_token"],
            },
            db=db,
        )
        APP_LOGGER.info(
            f"Shared auth registration complete: {db_user.username} (local ID: {db_user.id}, auth ID: {db_user.auth_user_id})"
        )
        return token_payload

    except HTTPException:
        raise
    except Exception as e:
        APP_LOGGER.error(f"Registration error for user {user.username}: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed",
        )


@router.post("/login", response_model=Token)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """Login via shared auth and sync the local Namo user mirror."""

    APP_LOGGER.info(f"Login attempt for user: {user.username}")

    try:
        token_payload = request_auth_token(user.username, user.password, "login")
        db_user = get_current_user(
            token_data={
                "username": user.username,
                "auth_user_id": _decode_token_user_id(token_payload["access_token"]),
                "token": token_payload["access_token"],
            },
            db=db,
        )
        APP_LOGGER.info(
            f"Shared auth login complete: {db_user.username} (local ID: {db_user.id}, auth ID: {db_user.auth_user_id})"
        )
        return token_payload

    except HTTPException:
        raise
    except Exception as e:
        APP_LOGGER.error(f"Login error for user {user.username}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login failed"
        )


@router.delete("/me")
def delete_current_user(
    current_user: User = Depends(get_current_user),
):
    """Account deletion must be handled by the shared auth service."""
    APP_LOGGER.info(
        f"Delete account requested for user {current_user.username}, but central auth owns account lifecycle"
    )
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Account deletion must be handled by the shared auth service",
    )


# GET /auth/users/search?q=ann&limit=20&after_username=anna&after_id=10
@router.get("/users/search", response_model=List[UserResponse])
def search_users(
    q: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    after_username: Optional[str] = None,
    after_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search users by username with keyset pagination."""
    query = db.query(User)

    if q:
        query = query.filter(User.username.ilike(f"%{q}%"))

    if after_username:
        if after_id is None:
            raise HTTPException(
                status_code=400, detail="after_id required with after_username"
            )
        after_username_lower = after_username.lower()
        query = query.filter(
            (func.lower(User.username) > after_username_lower)
            | (
                (func.lower(User.username) == after_username_lower)
                & (User.id > after_id)
            )
        )

    query = query.order_by(func.lower(User.username).asc(), User.id.asc())
    return query.limit(limit).all()


def _decode_token_user_id(access_token: str) -> int:
    from auth.auth_utils import verify_token
    from fastapi.security import HTTPAuthorizationCredentials

    token_data = verify_token(
        HTTPAuthorizationCredentials(scheme="Bearer", credentials=access_token)
    )
    return int(token_data["auth_user_id"])
