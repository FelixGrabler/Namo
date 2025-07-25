from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    Text,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

# Import read_secret from config
from config import read_secret


# Database configuration from environment variables and secrets
POSTGRES_USER = os.getenv("POSTGRES_USER", "namo_dev")
POSTGRES_DB = os.getenv("POSTGRES_DB", "namo_dev")
DATABASE_HOST = os.getenv("DATABASE_HOST", "db")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Get password from Docker secrets based on environment
if ENVIRONMENT == "production":
    POSTGRES_PASSWORD = read_secret("prod_postgres_password") or os.getenv(
        "POSTGRES_PASSWORD", "change_this_in_production"
    )
else:
    POSTGRES_PASSWORD = read_secret("dev_postgres_password") or os.getenv(
        "POSTGRES_PASSWORD", "dev_password_123"
    )

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DATABASE_HOST}:5432/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)

    # Relationship with votes
    votes = relationship("Vote", back_populates="user")


class Name(Base):
    __tablename__ = "names"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)  # e.g. 'Austria'
    name = Column(String, nullable=False)
    gender = Column(String, nullable=True)  # 'm' or 'f'
    rank = Column(Integer, nullable=True)
    count = Column(Integer, nullable=True)
    info = Column(JSONB, nullable=True)

    # Relationship with votes
    votes = relationship("Vote", back_populates="name")


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name_id = Column(Integer, ForeignKey("names.id"), nullable=False)
    vote = Column(Boolean, nullable=False)  # TRUE = like, FALSE = dislike

    # Relationships
    user = relationship("User", back_populates="votes")
    name = relationship("Name", back_populates="votes")

    # Unique constraint: one vote per name per user
    __table_args__ = (
        UniqueConstraint("user_id", "name_id", name="unique_user_name_vote"),
    )
