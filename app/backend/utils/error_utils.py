"""
Utility functions for error handling and logging throughout the application.
"""

import asyncio
from typing import Optional, Dict, Any
from fastapi import HTTPException

from utils.logging_config import ERROR_LOGGER, APP_LOGGER, log_exception
from utils.telegram_notifier import telegram_notifier


def handle_error(
    exception: Exception,
    context: str = "",
    send_telegram: bool = True,
    raise_http_exception: bool = True,
    status_code: int = 500,
) -> Dict[str, Any]:
    """
    Comprehensive error handling function.

    Args:
        exception: The exception that occurred
        context: Additional context about where the error occurred
        send_telegram: Whether to send a Telegram notification
        raise_http_exception: Whether to raise an HTTPException after logging
        status_code: HTTP status code to use if raising HTTPException

    Returns:
        Dictionary with error details
    """
    # Log the exception with full details
    error_details = log_exception(ERROR_LOGGER, exception, context)

    # Send Telegram notification if requested
    if send_telegram:
        try:
            telegram_notifier.send_error_notification_sync(error_details, context)
        except Exception as telegram_error:
            ERROR_LOGGER.error(
                f"Failed to send Telegram notification: {telegram_error}"
            )

    # Raise HTTPException if requested
    if raise_http_exception:
        raise HTTPException(
            status_code=status_code, detail="An internal error occurred"
        )

    return error_details


async def handle_error_async(
    exception: Exception,
    context: str = "",
    send_telegram: bool = True,
    raise_http_exception: bool = True,
    status_code: int = 500,
) -> Dict[str, Any]:
    """
    Async version of handle_error function.
    """
    # Log the exception with full details
    error_details = log_exception(ERROR_LOGGER, exception, context)

    # Send Telegram notification if requested
    if send_telegram:
        try:
            await telegram_notifier.send_error_notification(error_details, context)
        except Exception as telegram_error:
            ERROR_LOGGER.error(
                f"Failed to send Telegram notification: {telegram_error}"
            )

    # Raise HTTPException if requested
    if raise_http_exception:
        raise HTTPException(
            status_code=status_code, detail="An internal error occurred"
        )

    return error_details


def log_info(message: str, context: str = ""):
    """Log an info message with optional context."""
    log_message = f"{context}: {message}" if context else message
    APP_LOGGER.info(log_message)


def log_warning(message: str, context: str = ""):
    """Log a warning message with optional context."""
    log_message = f"{context}: {message}" if context else message
    APP_LOGGER.warning(log_message)


async def send_telegram_alert(message: str, is_critical: bool = False):
    """Send a custom Telegram alert message."""
    try:
        if is_critical:
            await telegram_notifier.send_critical_error_notification(message)
        else:
            await telegram_notifier.send_message(
                f"🔔 <b>NAMO API Alert</b>\n\n{message}"
            )
        APP_LOGGER.info("Custom Telegram alert sent successfully")
    except Exception as e:
        APP_LOGGER.error(f"Failed to send custom Telegram alert: {e}")


def send_telegram_alert_sync(message: str, is_critical: bool = False):
    """Synchronous version of send_telegram_alert."""
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_telegram_alert(message, is_critical))
    except RuntimeError:
        asyncio.run(send_telegram_alert(message, is_critical))
