import time
from datetime import datetime
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from typing import Callable

from utils.logging_config import REQUEST_LOGGER, ERROR_LOGGER, log_exception
from utils.telegram_notifier import telegram_notifier


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        # Get client info
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")

        try:
            response = await call_next(request)

            # Calculate processing time
            process_time = time.time() - start_time

            # Log the request
            log_entry = (
                f"Method: {request.method} | "
                f"URL: {request.url} | "
                f"Status: {response.status_code} | "
                f"Time: {process_time:.3f}s | "
                f"Client: {client_ip} | "
                f"User-Agent: {user_agent}"
            )

            REQUEST_LOGGER.info(log_entry)

            return response

        except Exception as e:
            # Calculate processing time even for errors
            process_time = time.time() - start_time

            # Log the failed request
            log_entry = (
                f"Method: {request.method} | "
                f"URL: {request.url} | "
                f"Status: 500 | "
                f"Time: {process_time:.3f}s | "
                f"Client: {client_ip} | "
                f"User-Agent: {user_agent} | "
                f"ERROR: {str(e)}"
            )

            REQUEST_LOGGER.error(log_entry)

            # Log the exception with full details
            error_details = log_exception(
                ERROR_LOGGER, e, f"Request failed: {request.method} {request.url}"
            )

            # Send Telegram notification for server errors
            try:
                await telegram_notifier.send_error_notification(
                    error_details, f"Request Error: {request.method} {request.url}"
                )
            except Exception as telegram_error:
                ERROR_LOGGER.error(
                    f"Failed to send Telegram notification: {telegram_error}"
                )

            # Re-raise the exception to be handled by FastAPI
            raise


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            # This catches any unhandled exceptions
            error_details = log_exception(
                ERROR_LOGGER,
                e,
                f"Unhandled exception in {request.method} {request.url}",
            )

            # Send Telegram notification
            try:
                await telegram_notifier.send_error_notification(
                    error_details,
                    f"Unhandled Exception: {request.method} {request.url}",
                )
            except Exception as telegram_error:
                ERROR_LOGGER.error(
                    f"Failed to send Telegram notification: {telegram_error}"
                )

            # Return a generic error response
            from fastapi.responses import JSONResponse

            return JSONResponse(
                status_code=500, content={"detail": "Internal server error"}
            )
