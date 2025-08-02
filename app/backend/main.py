from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
from contextlib import asynccontextmanager
import os
from datetime import datetime
from dotenv import load_dotenv
from datetime import datetime

from models.database import engine, SessionLocal, Base
from routes import auth, names, votes
from auth.auth_utils import verify_token
from init_db import init_db

# Import logging and middleware
from utils.logging_config import (
    setup_logging,
    APP_LOGGER,
    get_log_files_info,
    get_log_config_info,
    force_log_rotation,
)
from utils.middleware import RequestLoggingMiddleware, ErrorHandlingMiddleware
from utils.exception_handlers import http_exception_handler, general_exception_handler
from utils.telegram_notifier import telegram_notifier

# Load environment variables
load_dotenv()

# Note: Database tables will be created by init_db() during startup


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - Initialize database with data
    APP_LOGGER.info("Starting up: Initializing database...")
    init_db(force_reload=os.getenv("FORCE_DB_RELOAD", "false").lower() == "true")

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

# Add custom middleware (order matters - they execute in reverse order of addition)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(RequestLoggingMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
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
