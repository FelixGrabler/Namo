from pydantic_settings import BaseSettings
from typing import List, Optional
import os


def read_secret(secret_name: str) -> str:
    """Read secret from Docker secrets"""
    secret_path = f"/run/secrets/{secret_name}"
    if os.path.exists(secret_path):
        with open(secret_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""


def get_required_env(
    var_name: str, default: Optional[str] = None, allow_empty: bool = False
) -> str:
    """
    Get environment variable with validation.
    Throws an error in production if the variable is not set or empty.
    """
    value = os.getenv(var_name, default)
    environment = os.getenv("ENVIRONMENT", "development")

    if not value and not allow_empty:
        error_msg = f"❌ Environment variable '{var_name}' is required but not set!"
        print(error_msg)
        if environment == "production":
            raise RuntimeError(f"Missing required environment variable: {var_name}")
        else:
            print(f"⚠️  Using default value for '{var_name}': {repr(default)}")

    return value or ""


def get_required_secret(
    secret_name: str, fallback_default: Optional[str] = None
) -> str:
    """
    Get secret with validation.
    Throws an error in production if the secret is not available.
    """
    secret_value = read_secret(secret_name)
    environment = os.getenv("ENVIRONMENT", "development")

    if not secret_value:
        error_msg = f"❌ Secret '{secret_name}' is required but not available!"
        print(error_msg)
        if environment == "production":
            raise RuntimeError(f"Missing required secret: {secret_name}")
        else:
            print(f"⚠️  Using fallback value for secret '{secret_name}'")
            return fallback_default or ""

    return secret_value


class Settings(BaseSettings):
    # Database (from Docker Compose environment)
    postgres_user: str = get_required_env("POSTGRES_USER")
    postgres_db: str = get_required_env("POSTGRES_DB")

    # FastAPI (from Docker Compose environment)
    debug: bool = get_required_env("DEBUG", "true").lower() == "true"
    reload: bool = get_required_env("RELOAD", "true").lower() == "true"
    log_level: str = get_required_env("LOG_LEVEL", "debug")

    # JWT (from Docker Compose environment)
    algorithm: str = get_required_env("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(
        get_required_env("ACCESS_TOKEN_EXPIRE_MINUTES", "10000")
    )

    # CORS (from Docker Compose environment)
    cors_origins: str = get_required_env("CORS_ORIGINS", "http://localhost:5173")

    # Logging (from Docker Compose environment)
    log_max_size_mb: int = int(get_required_env("LOG_MAX_SIZE_MB", "10"))
    log_backup_count: int = int(get_required_env("LOG_BACKUP_COUNT", "3"))
    log_console: bool = get_required_env("LOG_CONSOLE", "true").lower() == "true"

    def get_cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into a list"""
        return [
            origin.strip() for origin in self.cors_origins.split(",") if origin.strip()
        ]

    def get_secret_key(self) -> str:
        """Get secret key from Docker secrets"""
        return get_required_secret("secret_key")

    def get_postgres_password(self) -> str:
        """Get postgres password from Docker secrets"""
        return get_required_secret("postgres_password")

    def get_telegram_bot_token(self) -> str:
        """Get telegram bot token from Docker secrets"""
        return get_required_secret("telegram_bot_token")

    def get_telegram_chat_id(self) -> str:
        """Get telegram chat ID from Docker secrets"""
        return get_required_secret("telegram_chat_id")

    def get_database_url(self) -> str:
        """Construct database URL using secrets"""
        password = self.get_postgres_password()
        return (
            f"postgresql://{self.postgres_user}:{password}@db:5432/{self.postgres_db}"
        )


# Global settings instance
settings = Settings()
