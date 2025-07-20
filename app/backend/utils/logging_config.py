import os
import logging
import traceback
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Create logs directory relative to the script location (works in Docker)
SCRIPT_DIR = Path(__file__).parent.parent.absolute()
LOGS_DIR = SCRIPT_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)


# Configure logging
def setup_logging():
    # Log rotation settings (configurable via environment variables)
    MAX_LOG_SIZE = (
        int(os.getenv("LOG_MAX_SIZE_MB", "10")) * 1024 * 1024
    )  # Default: 10 MB per file
    BACKUP_COUNT = int(
        os.getenv("LOG_BACKUP_COUNT", "3")
    )  # Default: Keep 3 backup files

    # Log level from environment (for production vs development)
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

    # Error log configuration
    error_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
    )

    # Request log configuration
    request_formatter = logging.Formatter("%(asctime)s - %(message)s")

    # Error logger with rotation
    error_logger = logging.getLogger("namo.errors")
    error_logger.setLevel(logging.ERROR)

    error_handler = RotatingFileHandler(
        LOGS_DIR / "errors.log", maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT
    )
    error_handler.setFormatter(error_formatter)
    error_logger.addHandler(error_handler)

    # Request logger with rotation
    request_logger = logging.getLogger("namo.requests")
    request_logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    request_handler = RotatingFileHandler(
        LOGS_DIR / "requests.log", maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT
    )
    request_handler.setFormatter(request_formatter)
    request_logger.addHandler(request_handler)

    # General app logger with rotation
    app_logger = logging.getLogger("namo.app")
    app_logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    app_handler = RotatingFileHandler(
        LOGS_DIR / "app.log", maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT
    )
    app_handler.setFormatter(error_formatter)
    app_logger.addHandler(app_handler)

    # Console handler for development (no rotation needed)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(error_formatter)
    # Only log to console in development or if explicitly enabled
    console_enabled = os.getenv("LOG_CONSOLE", "true").lower() == "true"
    if console_enabled:
        app_logger.addHandler(console_handler)

    return error_logger, request_logger, app_logger


def log_exception(logger, exception: Exception, context: str = ""):
    """Log an exception with full traceback and context."""
    error_details = {
        "timestamp": datetime.now().isoformat(),
        "exception_type": type(exception).__name__,
        "exception_message": str(exception),
        "context": context,
        "traceback": traceback.format_exc(),
    }

    log_message = f"""
==== EXCEPTION OCCURRED ====
Timestamp: {error_details['timestamp']}
Context: {error_details['context']}
Exception Type: {error_details['exception_type']}
Exception Message: {error_details['exception_message']}
Traceback:
{error_details['traceback']}
============================
"""

    logger.error(log_message)
    return error_details


def get_log_files_info():
    """Get information about current log files."""
    log_info = {}

    for log_file in ["errors.log", "requests.log", "app.log"]:
        log_path = LOGS_DIR / log_file
        if log_path.exists():
            stat = log_path.stat()
            log_info[log_file] = {
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "exists": True,
            }

            # Check for rotated files
            rotated_files = []
            for i in range(1, int(os.getenv("LOG_BACKUP_COUNT", "3")) + 1):
                rotated_path = LOGS_DIR / f"{log_file}.{i}"
                if rotated_path.exists():
                    rotated_stat = rotated_path.stat()
                    rotated_files.append(
                        {
                            "file": f"{log_file}.{i}",
                            "size_mb": round(rotated_stat.st_size / (1024 * 1024), 2),
                            "modified": datetime.fromtimestamp(
                                rotated_stat.st_mtime
                            ).isoformat(),
                        }
                    )

            if rotated_files:
                log_info[log_file]["rotated_files"] = rotated_files
        else:
            log_info[log_file] = {"exists": False}

    return log_info


def force_log_rotation():
    """Manually trigger log rotation for all loggers."""
    try:
        # Get all handlers that are RotatingFileHandler instances
        for logger_name in ["namo.errors", "namo.requests", "namo.app"]:
            logger = logging.getLogger(logger_name)
            for handler in logger.handlers:
                if isinstance(handler, RotatingFileHandler):
                    handler.doRollover()

        APP_LOGGER.info("Manual log rotation completed")
        return True
    except Exception as e:
        if "APP_LOGGER" in globals():
            APP_LOGGER.error(f"Failed to perform manual log rotation: {e}")
        return False


def get_log_config_info():
    """Get current logging configuration information."""
    max_size_mb = int(os.getenv("LOG_MAX_SIZE_MB", "10"))
    backup_count = int(os.getenv("LOG_BACKUP_COUNT", "3"))
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    console_enabled = os.getenv("LOG_CONSOLE", "true").lower() == "true"

    return {
        "max_file_size_mb": max_size_mb,
        "backup_count": backup_count,
        "total_files_per_log": backup_count + 1,  # including current file
        "log_level": log_level,
        "console_logging": console_enabled,
        "logs_directory": str(LOGS_DIR),
        "estimated_max_disk_usage_mb": max_size_mb
        * (backup_count + 1)
        * 3,  # 3 log types
    }


# Initialize loggers
ERROR_LOGGER, REQUEST_LOGGER, APP_LOGGER = setup_logging()
