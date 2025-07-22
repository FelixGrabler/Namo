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
        ERROR_LOGGER.error(f"Failed to get info for name {name}: {str(e)}")
        return None


def update_name_info(limit_to_first: bool = True):
    db: Session = SessionLocal()

    try:
        query = db.query(Name).filter(Name.info.is_(None))

        if limit_to_first:
            names = query.limit(1).all()
            log_info("Processing only the first name as requested")
        else:
            names = query.all()

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
                log_warning(f"No info data available for name: {name}")

            if limit_to_first:
                log_info("Stopping after first element as requested")
                break

    except Exception as e:
        ERROR_LOGGER.error(f"Error during name info update: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


def main():
    log_info("Starting name info database update process")
    update_name_info(limit_to_first=True)
    log_info("Name info database update process completed")


if __name__ == "__main__":
    main()
