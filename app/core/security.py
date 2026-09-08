"""
Authentication dependencies for the four security modes:
  1. No authentication  (public)
  2. Bearer token       (Authorization: Bearer <token>)
  3. API key header     (X-API-Key: <key>)
  4. HTTP Basic         (Authorization: Basic <b64>)

FastAPI security utilities are used so that each scheme is reflected
in the generated OpenAPI / Swagger documentation.
"""
import secrets

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials, HTTPBearer

from app.core.config import settings

# ── scheme definitions ────────────────────────────────────────────────────────

bearer_scheme = HTTPBearer(auto_error=False)
api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)
basic_scheme = HTTPBasic(auto_error=False)


# ── helpers ───────────────────────────────────────────────────────────────────

def _auth_error(code: str, message: str, status_code: int = status.HTTP_401_UNAUTHORIZED):
    raise HTTPException(
        status_code=status_code,
        detail={
            "error": {
                "code": code,
                "message": message,
                "status": status_code,
            }
        },
        headers={"WWW-Authenticate": "Bearer"},
    )


# ── dependency functions ──────────────────────────────────────────────────────

def require_bearer(credentials=Security(bearer_scheme)):
    """Validate Bearer token."""
    if credentials is None:
        _auth_error("AUTHENTICATION_REQUIRED", "Bearer token is required.")
    if not secrets.compare_digest(credentials.credentials, settings.BEARER_TOKEN):
        _auth_error("INVALID_BEARER_TOKEN", "Invalid bearer token.")
    return credentials.credentials


def require_api_key(api_key: str = Security(api_key_scheme)):
    """Validate X-API-Key header."""
    if api_key is None:
        _auth_error("AUTHENTICATION_REQUIRED", "API key header X-API-Key is required.")
    if not secrets.compare_digest(api_key, settings.API_KEY):
        _auth_error("INVALID_API_KEY", "Invalid API key.")
    return api_key


def require_basic(credentials: HTTPBasicCredentials = Security(basic_scheme)):
    """Validate HTTP Basic credentials."""
    if credentials is None:
        _auth_error("AUTHENTICATION_REQUIRED", "HTTP Basic credentials are required.")
    username_ok = secrets.compare_digest(credentials.username, settings.BASIC_USERNAME)
    password_ok = secrets.compare_digest(credentials.password, settings.BASIC_PASSWORD)
    if not (username_ok and password_ok):
        _auth_error("INVALID_BASIC_CREDENTIALS", "Invalid username or password.")
    return credentials.username
