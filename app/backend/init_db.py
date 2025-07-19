"""
Database initialization script with sample data
Supports both hardcoded data and CSV loading
"""

import csv
import os
from pathlib import Path
from sqlalchemy.orm import Session
from models.database import engine, SessionLocal, Base, User, Name
from auth.auth_utils import get_password_hash


def load_names_from_csv(file_path: str) -> list:
    """Load names from CSV file."""
    names = []
    if not os.path.exists(file_path):
        print(f"CSV file not found: {file_path}")
        return names

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = Name(
                    source=row["source"],
                    name=row["name"],
                    gender=row.get("gender", "").lower() if row.get("gender") else None,
                    rank=(
                        int(row["rank"])
                        if row.get("rank") and row["rank"].strip()
                        else None
                    ),
                    count=(
                        int(row["count"])
                        if row.get("count") and row["count"].strip()
                        else None
                    ),
                )
                names.append(name)
        print(f"Loaded {len(names)} names from {file_path}")
    except Exception as e:
        print(f"Error loading CSV: {e}")

    return names


def get_sample_names():
    """Get sample names (fallback if no CSV)."""
    return [
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


def init_db(force_reload: bool = False):
    """Initialize database with tables and sample data."""
    # Create all tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if we already have data
        if not force_reload and db.query(Name).first() is not None:
            print("Database already has data, skipping initialization.")
            print("Use --force to reload data anyway.")
            return

        # Clear existing data if force_reload
        if force_reload:
            print("Force reload: Clearing existing data...")
            db.query(Name).delete()
            db.query(User).delete()
            db.commit()

        # Create sample users
        users = [
            User(username="admin", password_hash=get_password_hash("admin123")),
            User(username="testuser", password_hash=get_password_hash("password123")),
        ]

        for user in users:
            db.add(user)

        # Load names from CSV or use sample data
        csv_path = "data/names.csv"
        names = load_names_from_csv(csv_path)

        if not names:
            print("No CSV data found, using sample data...")
            names = get_sample_names()

        for name in names:
            db.add(name)

        db.commit()
        print(f"Database initialized with {len(users)} users and {len(names)} names.")

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    import sys

    force_reload = "--force" in sys.argv
    init_db(force_reload=force_reload)
