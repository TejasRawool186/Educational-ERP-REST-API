"""
NextGen Institute of AI & Technology — Educational ERP REST API
FastAPI application entry point.
"""
import logging
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import Base, engine
import app.core.database as _db_module
from app.routers import health, public, bearer, apikey, basic, analytics

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


# ── Lifespan ──────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Always use the current engine from the database module so tests can
    # substitute a SQLite engine before startup without patching globals.
    try:
        Base.metadata.create_all(bind=_db_module.engine)
        logger.info("Database tables verified / created.")
    except Exception as exc:
        logger.warning("Could not create tables at startup: %s", exc)
    yield
    logger.info("Shutdown complete.")


# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "**NextGen Institute of AI & Technology (NGIAT)** — Centralized Educational ERP REST API. "
        "Large synthetic dataset for testing REST ingestion, OpenAPI discovery, "
        "authentication validation, pagination, filtering, and schema discovery. "
        "Supports four authentication modes: No Auth · Bearer Token · API Key · HTTP Basic."
    ),
    openapi_tags=[
        {"name": "Health", "description": "Health and root endpoints (no auth)"},
        {"name": "Public", "description": "Public reference data — no authentication required"},
        {"name": "Bearer Auth", "description": "Student and academic data — Bearer token required"},
        {"name": "API Key Auth", "description": "Operational data — X-API-Key header required"},
        {"name": "Basic Auth", "description": "Career data — HTTP Basic required"},
        {"name": "Analytics", "description": "Aggregation endpoints — Bearer token required"},
    ],
    swagger_ui_parameters={"persistAuthorization": True},
    lifespan=lifespan,
)

# ── Security schemes — exposed in OpenAPI ─────────────────────────────────────
from fastapi.openapi.utils import get_openapi


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
    )
    schema.setdefault("components", {}).setdefault("securitySchemes", {})
    schema["components"]["securitySchemes"].update(
        {
            "BearerAuth": {"type": "http", "scheme": "bearer"},
            "ApiKeyAuth": {"type": "apiKey", "in": "header", "name": "X-API-Key"},
            "BasicAuth": {"type": "http", "scheme": "basic"},
        }
    )
    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi  # type: ignore[method-assign]

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


# ── Request logging + X-Request-ID ───────────────────────────────────────────
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start = time.perf_counter()
    response: Response = await call_next(request)
    elapsed_ms = round((time.perf_counter() - start) * 1000)
    # Never log Authorization headers (SEC-04)
    logger.info(
        "%s %s %s %dms request_id=%s",
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
        request_id,
    )
    response.headers["X-Request-ID"] = request_id
    return response


# ── Global exception handler ──────────────────────────────────────────────────
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An internal error occurred.",
                "status": 500,
            }
        },
    )


# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(health.router)
app.include_router(public.router)
app.include_router(bearer.router)
app.include_router(analytics.router)
app.include_router(apikey.router)
app.include_router(basic.router)
