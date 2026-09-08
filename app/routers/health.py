"""
Health and root endpoints — no authentication required.
Used by Render health checks and UptimeRobot external monitoring.

/health  — performs a real SELECT 1 database ping.
           Returns 200 when healthy, 503 when the database is unreachable.
           Must remain lightweight — no large table queries.
"""
import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.core.config import settings
from app.core.database import SessionLocal

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Health"])


@router.get("/", summary="Root")
def root():
    """Public root endpoint — returns API identity and navigation links."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "institution": settings.INSTITUTION_NAME,
        "short_name": settings.INSTITUTION_SHORT,
        "status": "operational",
        "documentation": "/docs",
        "openapi": "/openapi.json",
        "redoc": "/redoc",
    }


@router.get("/health", summary="Health Check")
def health():
    """
    Lightweight health check used by:
      - Render Web Service health check path
      - UptimeRobot HTTP(s) monitor

    Executes SELECT 1 to confirm the database is reachable.
    Returns HTTP 200 when healthy, HTTP 503 when the database is unavailable.
    Never queries large tables. Never returns secrets.
    """
    db_status = "unavailable"
    try:
        db = SessionLocal()
        try:
            db.execute(text("SELECT 1"))
            db_status = "healthy"
        finally:
            db.close()
    except Exception as exc:
        logger.warning("Health check: database unreachable — %s", exc)

    is_healthy = db_status == "healthy"
    payload = {
        "status": "healthy" if is_healthy else "unhealthy",
        "service": settings.SERVICE_NAME,
        "version": settings.APP_VERSION,
        "database": db_status,
    }
    return JSONResponse(
        status_code=200 if is_healthy else 503,
        content=payload,
    )
