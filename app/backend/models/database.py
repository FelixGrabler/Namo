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
from dotenv import load_dotenv

load_dotenv()

# Database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:password@localhost:5432/namo"
)

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
