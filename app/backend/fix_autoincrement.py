#!/usr/bin/env python3
"""
Database migration script to fix autoincrement on existing tables.
This will add autoincrement to the id columns without losing data.
"""

import os
import sys
from sqlalchemy import create_engine, text
from config import get_required_env, get_required_secret


def get_database_url():
    """Get database URL using the same config as the app"""
    POSTGRES_USER = get_required_env("POSTGRES_USER")
    POSTGRES_DB = get_required_env("POSTGRES_DB")
    DATABASE_HOST = get_required_env("DATABASE_HOST")
    POSTGRES_PASSWORD = get_required_secret("postgres_password")

    return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DATABASE_HOST}:5432/{POSTGRES_DB}"


def fix_autoincrement():
    """Fix autoincrement on all tables"""
    try:
        engine = create_engine(get_database_url())

        with engine.connect() as conn:
            # Start a transaction
            trans = conn.begin()

            try:
                print("Checking current table structure...")

                # Check if tables exist and their current structure
                result = conn.execute(
                    text(
                        """
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name IN ('users', 'names', 'votes')
                """
                    )
                )

                existing_tables = [row[0] for row in result]
                print(f"Found tables: {existing_tables}")

                # Fix each table's id column to be auto-incrementing
                for table_name in ["users", "names", "votes"]:
                    if table_name in existing_tables:
                        print(f"Fixing autoincrement for {table_name} table...")

                        # Get the current maximum ID
                        max_id_result = conn.execute(
                            text(f"SELECT COALESCE(MAX(id), 0) FROM {table_name}")
                        )
                        max_id = max_id_result.scalar()
                        print(f"Current max ID in {table_name}: {max_id}")

                        # Create or update the sequence
                        sequence_name = f"{table_name}_id_seq"

                        # Drop sequence if exists and recreate it
                        conn.execute(
                            text(f"DROP SEQUENCE IF EXISTS {sequence_name} CASCADE")
                        )
                        conn.execute(
                            text(f"CREATE SEQUENCE {sequence_name} START {max_id + 1}")
                        )

                        # Set the default value for the id column to use the sequence
                        conn.execute(
                            text(
                                f"ALTER TABLE {table_name} ALTER COLUMN id SET DEFAULT nextval('{sequence_name}')"
                            )
                        )

                        # Set the sequence owner
                        conn.execute(
                            text(
                                f"ALTER SEQUENCE {sequence_name} OWNED BY {table_name}.id"
                            )
                        )

                        print(f"✅ Fixed autoincrement for {table_name}")
                    else:
                        print(f"⚠️  Table {table_name} not found, skipping...")

                # Commit the transaction
                trans.commit()
                print("✅ All autoincrement fixes applied successfully!")

            except Exception as e:
                # Rollback on error
                trans.rollback()
                print(f"❌ Error during migration: {e}")
                raise

    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("🔧 Starting autoincrement fix migration...")
    fix_autoincrement()
    print("🎉 Migration completed!")
