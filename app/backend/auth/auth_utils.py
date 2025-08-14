from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from models.database import User, SessionLocal
from config import get_required_env, get_required_secret


# Configuration from environment variables and secrets
def get_secret_key():
    """Get secret key lazily to avoid import-time errors"""
    return get_required_secret("secret_key")


ALGORITHM = get_required_env("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    get_required_env("ACCESS_TOKEN_EXPIRE_MINUTES", "10080")
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    try:
        to_encode = data.copy()
        now = datetime.now(timezone.utc)

        if expires_delta:
            expire = now + expires_delta
        else:
            expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        # Add standard JWT claims and custom data
        to_encode.update(
            {
                "sub": data.get("username"),  # subject (username)
                "user_id": data.get("user_id"),  # user ID
                "iat": int(now.timestamp()),  # issued at timestamp
                "exp": int(expire.timestamp()),  # expiration timestamp
            }
        )

        secret_key = get_secret_key()
        if not secret_key:
            raise ValueError("Secret key not available for JWT signing")

        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print(f"Error creating access token: {e}")
        raise


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify and decode JWT token."""
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        secret_key = get_secret_key()
        if not secret_key:
            raise ValueError("Secret key not available for JWT verification")

        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        user_id: Optional[int] = payload.get("user_id")

        if username is None or user_id is None:
            raise credentials_exception

        return {"username": username, "user_id": user_id}
    except ValueError as e:
        print(f"JWT verification error: {e}")
        raise credentials_exception
    except JWTError as exc:
        print(f"JWT decode error: {exc}")
        raise credentials_exception from exc


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token_data: dict = Depends(verify_token), db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user."""
    username = token_data["username"]
    user_id = token_data["user_id"]

    user = db.query(User).filter(User.username == username, User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user
