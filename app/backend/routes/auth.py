from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from auth.auth_utils import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_db,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from models.database import User
from schemas.schemas import UserCreate, UserResponse, UserLogin, Token
from utils.logging_config import APP_LOGGER

router = APIRouter()


@router.post("/register", response_model=Token)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and return an access token."""

    APP_LOGGER.info(f"Registration attempt for user: {user.username}")

    try:
        # Check if user already exists
        db_user = db.query(User).filter(User.username == user.username).first()
        if db_user:
            APP_LOGGER.warning(
                f"Registration failed - user already exists: {user.username}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )

        # Hash password and create user
        hashed_password = get_password_hash(user.password)
        new_user = User(username=user.username, password_hash=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        APP_LOGGER.info(
            f"User created successfully: {user.username} (ID: {new_user.id})"
        )

        # Create access token
        access_token = create_access_token(
            data={"username": new_user.username, "user_id": new_user.id}
        )

        APP_LOGGER.info(f"Access token created for user: {user.username}")

        return {"access_token": access_token, "token_type": "bearer"}

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
    """Login user and return access token."""

    APP_LOGGER.info(f"Login attempt for user: {user.username}")

    try:
        # Authenticate user
        db_user = db.query(User).filter(User.username == user.username).first()
        if not db_user:
            APP_LOGGER.warning(f"Login failed - user not found: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not verify_password(user.password, str(db_user.password_hash)):
            APP_LOGGER.warning(
                f"Login failed - invalid password for user: {user.username}"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        APP_LOGGER.info(
            f"User authenticated successfully: {user.username} (ID: {db_user.id})"
        )

        # Create access token
        access_token = create_access_token(
            data={"username": db_user.username, "user_id": db_user.id}
        )

        APP_LOGGER.info(f"Access token created for user: {user.username}")

        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        APP_LOGGER.error(f"Login error for user {user.username}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login failed"
        )
