from typing import Any, Optional
import requests
from jose import JWTError, jwt
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
AUTH_SERVICE_URL = get_required_env("AUTH_SERVICE_URL", "http://shared-auth:8000/api/auth")

security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)


def fetch_auth_user(token: str) -> dict[str, Any]:
    """Resolve the current user from the shared auth service."""
    try:
        response = requests.get(
            f"{AUTH_SERVICE_URL.rstrip('/')}/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Shared authentication service is unavailable",
        ) from exc

    try:
        payload = response.json()
    except ValueError:
        payload = {"detail": response.text}

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=payload.get("detail", "Could not validate credentials"),
        )

    user_id = payload.get("id")
    username = payload.get("username")
    if user_id is None or username is None:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Shared authentication service returned invalid user data",
        )

    return {"username": str(username), "auth_user_id": int(user_id), "token": token}


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
        auth_user_id: Optional[int] = payload.get("user_id")

        if username is None or auth_user_id is None:
            raise credentials_exception

        return {"username": username, "auth_user_id": auth_user_id, "token": token}
    except ValueError as e:
        print(f"JWT verification error: {e}")
    except JWTError as exc:
        print(f"JWT decode error: {exc}")

    try:
        return fetch_auth_user(token)
    except HTTPException as exc:
        if exc.status_code == status.HTTP_401_UNAUTHORIZED:
            raise credentials_exception from exc
        raise


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
    auth_user_id = token_data["auth_user_id"]

    user = db.query(User).filter(User.auth_user_id == auth_user_id).first()
    if user is not None:
        if user.username != username:
            user.username = username
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    fallback_user = db.query(User).filter(User.username == username).first()
    if fallback_user is not None:
        fallback_user.auth_user_id = auth_user_id
        fallback_user.username = username
        db.add(fallback_user)
        db.commit()
        db.refresh(fallback_user)
        return fallback_user

    new_user = User(
        auth_user_id=auth_user_id,
        username=username,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def verify_optional_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(optional_security),
):
    """Return token data when a bearer token is present, otherwise allow anonymous access."""
    if credentials is None:
        return None
    return verify_token(credentials)


def get_optional_current_user(
    token_data: Optional[dict] = Depends(verify_optional_token),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """Resolve the current user when authenticated, otherwise return None."""
    if token_data is None:
        return None

    username = token_data["username"]
    auth_user_id = token_data["auth_user_id"]

    user = db.query(User).filter(User.auth_user_id == auth_user_id).first()
    if user is not None:
        if user.username != username:
            user.username = username
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    fallback_user = db.query(User).filter(User.username == username).first()
    if fallback_user is not None:
        fallback_user.auth_user_id = auth_user_id
        fallback_user.username = username
        db.add(fallback_user)
        db.commit()
        db.refresh(fallback_user)
        return fallback_user

    new_user = User(
        auth_user_id=auth_user_id,
        username=username,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def request_auth_token(username: str, password: str, endpoint: str) -> dict:
    try:
        response = requests.post(
            f"{AUTH_SERVICE_URL.rstrip('/')}/{endpoint.lstrip('/')}",
            json={"username": username, "password": password},
            timeout=10,
        )
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Shared authentication service is unavailable",
        ) from exc

    try:
        payload = response.json()
    except ValueError:
        payload = {"detail": response.text}

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=payload.get("detail", "Authentication request failed"),
        )

    token = payload.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Shared authentication service returned no token",
        )
    return payload
