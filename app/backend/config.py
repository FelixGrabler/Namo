from pydantic_settings import BaseSettings
from typing import List
import os


def read_secret(secret_name: str) -> str:
    """Read secret from Docker secrets"""
    secret_path = f"/run/secrets/{secret_name}"
    if os.path.exists(secret_path):
        with open(secret_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""


class Settings(BaseSettings):
    # Database (from Docker Compose environment)
    postgres_user: str = os.getenv("POSTGRES_USER", "namo_dev")
    postgres_db: str = os.getenv("POSTGRES_DB", "namo_dev")

    # FastAPI (from Docker Compose environment)
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    reload: bool = os.getenv("RELOAD", "true").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "debug")

    # JWT (from Docker Compose environment)
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )

    # CORS (from Docker Compose environment)
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost:5173")

    # Logging (from Docker Compose environment)
    log_max_size_mb: int = int(os.getenv("LOG_MAX_SIZE_MB", "10"))
    log_backup_count: int = int(os.getenv("LOG_BACKUP_COUNT", "3"))
    log_console: bool = os.getenv("LOG_CONSOLE", "true").lower() == "true"

    def get_cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into a list"""
        return [
            origin.strip() for origin in self.cors_origins.split(",") if origin.strip()
        ]

    def get_secret_key(self) -> str:
        """Get secret key from Docker secrets"""
        environment = os.getenv("ENVIRONMENT", "development")
        if environment == "production":
            return read_secret("prod_secret_key")
        else:
            return (
                read_secret("dev_secret_key")
                or "dev_secret_key_not_for_production_use_only"
            )

    def get_postgres_password(self) -> str:
        """Get postgres password from Docker secrets"""
        environment = os.getenv("ENVIRONMENT", "development")
        if environment == "production":
            return read_secret("prod_postgres_password")
        else:
            return read_secret("dev_postgres_password") or "dev_password_123"

    def get_telegram_bot_token(self) -> str:
        """Get telegram bot token from Docker secrets"""
        environment = os.getenv("ENVIRONMENT", "development")
        if environment == "production":
            return read_secret("prod_telegram_bot_token")
        else:
            return read_secret("dev_telegram_bot_token")

    def get_telegram_chat_id(self) -> str:
        """Get telegram chat ID from Docker secrets"""
        environment = os.getenv("ENVIRONMENT", "development")
        if environment == "production":
            return read_secret("prod_telegram_chat_id")
        else:
            return read_secret("dev_telegram_chat_id")

    def get_database_url(self) -> str:
        """Construct database URL using secrets"""
        password = self.get_postgres_password()
        return (
            f"postgresql://{self.postgres_user}:{password}@db:5432/{self.postgres_db}"
        )


# Global settings instance
settings = Settings()
