from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from datetime import datetime

from models.database import engine, SessionLocal, Base
from routes import auth, names, votes
from init_db import init_db

# Import logging and middleware
from utils.logging_config import (
    setup_logging,
    APP_LOGGER,
    get_log_files_info,
    get_log_config_info,
    force_log_rotation,
)
from utils.logging_config import REQUEST_LOGGER, ERROR_LOGGER, log_exception
from utils.exception_handlers import http_exception_handler, general_exception_handler

# Load environment variables
load_dotenv()

# Note: Database tables will be created by init_db() during startup


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - Initialize database with data
    environment = os.getenv("ENVIRONMENT", "development").lower()
    init_on_startup = os.getenv("INIT_DB_ON_STARTUP")
    if init_on_startup is None:
        init_on_startup = "false" if environment == "production" else "true"

    # Always ensure tables exist; serialize with an advisory lock to avoid race
    # conditions when running multiple gunicorn workers.
    try:
        with engine.begin() as conn:
            conn.execute(text("SELECT pg_advisory_lock(424242)"))

            # If a previous concurrent startup left orphaned sequences (but no table),
            # drop them so create_all can succeed.
            for table_name, seq_name in (
                ("users", "users_id_seq"),
                ("names", "names_id_seq"),
                ("votes", "votes_id_seq"),
            ):
                table_exists = conn.execute(
                    text("SELECT to_regclass(:table_name)"),
                    {"table_name": f"public.{table_name}"},
                ).scalar()
                if table_exists is None:
                    conn.execute(
                        text("DROP SEQUENCE IF EXISTS " + seq_name)
                    )

            Base.metadata.create_all(bind=conn)
            conn.execute(text("SELECT pg_advisory_unlock(424242)"))
        APP_LOGGER.info("Database tables created or verified.")
    except Exception as exc:
        APP_LOGGER.warning("Database table creation skipped: %s", exc)

    if init_on_startup.lower() == "true":
        APP_LOGGER.info("Starting up: Initializing database...")
        init_db(force_reload=os.getenv("FORCE_DB_RELOAD", "false").lower() == "true")
    else:
        APP_LOGGER.info("Starting up: Skipping database initialization.")

    yield

    # Shutdown
    APP_LOGGER.info("Shutting down...")


app = FastAPI(
    title="Namo API",
    description="A name voting application API with comprehensive logging",
    version="1.0.0",
    lifespan=lifespan,
)

# Add error handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Request logging middleware (avoids BaseHTTPMiddleware streaming issues)
@app.middleware("http")
async def request_logging_middleware(request, call_next):
    start_time = datetime.now()
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")

    try:
        response = await call_next(request)
    except Exception as exc:
        process_time = (datetime.now() - start_time).total_seconds()
        log_entry = (
            f"Method: {request.method} | "
            f"URL: {request.url} | "
            f"Status: 500 | "
            f"Time: {process_time:.3f}s | "
            f"Client: {client_ip} | "
            f"User-Agent: {user_agent} | "
            f"ERROR: {str(exc)}"
        )
        REQUEST_LOGGER.error(log_entry)
        log_exception(
            ERROR_LOGGER, exc, f"Request failed: {request.method} {request.url}"
        )
        raise

    process_time = (datetime.now() - start_time).total_seconds()
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

# CORS middleware
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in cors_origins],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(names.router, prefix="/api/names", tags=["names"])
app.include_router(votes.router, prefix="/api/votes", tags=["votes"])


@app.get("/")
async def root():
    APP_LOGGER.info("Root endpoint accessed")
    return {"message": "Welcome to our Namo API"}


@app.get("/health")
async def health_check():
    APP_LOGGER.info("Health check endpoint accessed")
    return {"status": "healthy", "timestamp": "2025-01-21"}


@app.get("/admin/logs/info")
async def get_logs_info():
    """Get information about log files and configuration."""
    APP_LOGGER.info("Log info endpoint accessed")
    return {
        "config": get_log_config_info(),
        "files": get_log_files_info(),
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/admin/logs/rotate")
async def rotate_logs():
    """Manually trigger log rotation."""
    APP_LOGGER.info("Manual log rotation requested")
    success = force_log_rotation()
    return {
        "success": success,
        "message": "Log rotation completed" if success else "Log rotation failed",
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    APP_LOGGER.info("Starting Namo API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
