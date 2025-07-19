"""
Database initialization script with sample data
"""

from sqlalchemy.orm import Session
from models.database import engine, SessionLocal, Base, User, Name
from auth.auth_utils import get_password_hash


def init_db():
    """Initialize database with tables and sample data."""
    # Create all tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if we already have data
        if db.query(User).first() is not None:
            print("Database already has data, skipping initialization.")
            return

        # Create sample users
        users = [
            User(username="admin", password_hash=get_password_hash("admin123")),
            User(username="testuser", password_hash=get_password_hash("password123")),
        ]

        for user in users:
            db.add(user)

        # Create sample names
        names = [
            Name(source="Austria", name="Emma", gender="f", rank=1, count=1200),
            Name(source="Austria", name="Anna", gender="f", rank=2, count=1100),
            Name(source="Austria", name="Liam", gender="m", rank=1, count=1300),
            Name(source="Austria", name="Noah", gender="m", rank=2, count=1250),
            Name(source="Germany", name="Sofia", gender="f", rank=1, count=2000),
            Name(source="Germany", name="Maria", gender="f", rank=2, count=1900),
            Name(source="Germany", name="Leon", gender="m", rank=1, count=2100),
            Name(source="Germany", name="Ben", gender="m", rank=2, count=2050),
            Name(source="Switzerland", name="Mia", gender="f", rank=1, count=800),
            Name(source="Switzerland", name="Elena", gender="f", rank=2, count=750),
            Name(source="Switzerland", name="David", gender="m", rank=1, count=850),
            Name(source="Switzerland", name="Julian", gender="m", rank=2, count=800),
        ]

        for name in names:
            db.add(name)

        db.commit()
        print("Database initialized with sample data.")

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
