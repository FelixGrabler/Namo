from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os

from models.database import User, SessionLocal

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "default")
if not SECRET_KEY or SECRET_KEY == "default":
    raise RuntimeError("SECRET_KEY environment variable not set")

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", str(7 * 24 * 60))
)  # Default: 7 days

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
    to_encode = data.copy()
    now = datetime.now(timezone.utc)

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add standard JWT claims and custom data
    print(f"Current time (now): {now.isoformat()}")
    print(f"Expiration time (exp): {expire.isoformat()}")
    to_encode.update(
        {
            "sub": data.get("username"),  # subject (username)
            "user_id": data.get("user_id"),  # user ID
            "iat": int(now.timestamp()),  # issued at timestamp
            "exp": int(expire.timestamp()),  # expiration timestamp
        }
    )

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify and decode JWT token."""
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        user_id: Optional[int] = payload.get("user_id")
        exp_timestamp: Optional[int] = payload.get("exp")

        print(f"Decoded token 'iat' (now): {datetime.now(timezone.utc).isoformat()}")
        if exp_timestamp:
            print(f"Decoded token 'exp': {datetime.fromtimestamp(exp_timestamp, tz=timezone.utc).isoformat()}")

        if username is None or user_id is None:
            raise credentials_exception

        # Calculate and print how long the token still lasts
        if exp_timestamp:
            now = datetime.now(timezone.utc)
            exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            time_remaining = exp_datetime - now

            if time_remaining.total_seconds() > 0:
                days = time_remaining.days
                hours, remainder = divmod(time_remaining.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                print(
                    f"Token for user '{username}' (ID: {user_id}) expires in: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
                )
            else:
                print(f"Token for user '{username}' (ID: {user_id}) has expired")

        return {"username": username, "user_id": user_id}
    except JWTError as exc:
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
