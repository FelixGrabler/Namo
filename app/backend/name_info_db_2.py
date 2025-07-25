#!/usr/bin/env python3

import sys
import os
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from models.database import SessionLocal, Name
from utils.wikionary_fetcher import extract_name_info
from utils.error_utils import log_info, log_warning
from utils.logging_config import ERROR_LOGGER

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_name_info(name: str) -> Optional[Dict[str, Any]]:
    try:
        return extract_name_info(name)
    except Exception as e:
        ERROR_LOGGER.error("Failed to get info for name %s: %s", name, str(e))
        return None


def needs_info_update(name_record):
    """Check if a name record needs info update"""
    if name_record.info is None:
        return True
    if name_record.info == {}:
        return True
    # Check if info only contains 'ipa' key with value "…" (three dots)
    if (
        isinstance(name_record.info, dict)
        and len(name_record.info) == 1
        and "ipa" in name_record.info
        and name_record.info["ipa"] == "…"
    ):
        return True
    return False


def update_name_info(limit_to_first: bool = True):
    db: Session = SessionLocal()

    try:
        # Get all names and filter in Python since JSON filtering can be complex in SQLAlchemy
        all_names = db.query(Name).order_by(Name.rank).all()

        # Filter names that need info update
        names = [name for name in all_names if needs_info_update(name)]

        log_info(f"Total {len(names)} names to process")

        if limit_to_first and names:
            names = names[:1]
            log_info("Processing only the first name as requested")

        if not names:
            log_info("No names found without info data")
            return

        log_info(f"Found {len(names)} names to process")

        for i, name_record in enumerate(names, 1):
            name = name_record.name
            print(f"Processing name {i}/{len(names)}: {name}")

            info_data = get_name_info(name)

            if info_data:
                name_record.info = info_data
                db.commit()
                log_info(f"Successfully updated info for name: {name}")
            else:
                # Store empty JSON object to mark as processed but no data available
                name_record.info = {}
                db.commit()
                log_warning(
                    f"No info data available for name: {name} - marked as processed"
                )

            if limit_to_first:
                log_info("Stopping after first element as requested")
                break

    except Exception as e:
        ERROR_LOGGER.error("Error during name info update: %s", str(e))
        db.rollback()
        raise
    finally:
        db.close()


def main():
    log_info("Starting name info database update process")
    update_name_info(limit_to_first=False)
    log_info("Name info database update process completed")


if __name__ == "__main__":
    main()
