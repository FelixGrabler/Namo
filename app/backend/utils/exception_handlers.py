from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Union
import traceback

from utils.logging_config import ERROR_LOGGER, log_exception
from utils.telegram_notifier import telegram_notifier


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions with logging."""
    # Log HTTP errors (4xx and 5xx)
    if exc.status_code >= 500:
        error_details = {
            "timestamp": (
                str(request.state.timestamp)
                if hasattr(request.state, "timestamp")
                else "unknown"
            ),
            "exception_type": "HTTPException",
            "exception_message": exc.detail,
            "status_code": exc.status_code,
            "url": str(request.url),
            "method": request.method,
            "traceback": traceback.format_exc(),
        }

        log_exception(
            ERROR_LOGGER,
            exc,
            f"HTTP {exc.status_code} error in {request.method} {request.url}",
        )

        # Send Telegram notification for 5xx errors
        try:
            await telegram_notifier.send_error_notification(
                error_details,
                f"HTTP {exc.status_code} Error: {request.method} {request.url}",
            )
        except Exception as telegram_error:
            ERROR_LOGGER.error(
                f"Failed to send Telegram notification: {telegram_error}"
            )

    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all other exceptions with logging and Telegram notification."""
    error_details = log_exception(
        ERROR_LOGGER, exc, f"Unhandled exception in {request.method} {request.url}"
    )

    # Send Telegram notification
    try:
        await telegram_notifier.send_error_notification(
            error_details, f"Unhandled Exception: {request.method} {request.url}"
        )
    except Exception as telegram_error:
        ERROR_LOGGER.error(f"Failed to send Telegram notification: {telegram_error}")

    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
