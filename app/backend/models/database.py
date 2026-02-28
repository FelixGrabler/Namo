import os

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

# Import helper functions from config
from config import get_required_env, get_required_secret


# Database configuration from environment variables and secrets
POSTGRES_USER = get_required_env("POSTGRES_USER")
POSTGRES_DB = get_required_env("POSTGRES_DB")
DATABASE_HOST = get_required_env("DATABASE_HOST")

# Get password from Docker secrets
POSTGRES_PASSWORD = get_required_secret("postgres_password")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DATABASE_HOST}:5432/{POSTGRES_DB}"

POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "2"))
POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))
POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "1800"))

engine = create_engine(
    DATABASE_URL,
    pool_size=POOL_SIZE,
    max_overflow=MAX_OVERFLOW,
    pool_timeout=POOL_TIMEOUT,
    pool_recycle=POOL_RECYCLE,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    auth_user_id = Column(Integer, unique=True, nullable=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)

    # Relationship with votes
    votes = relationship("Vote", back_populates="user")


class Name(Base):
    __tablename__ = "names"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
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

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
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
