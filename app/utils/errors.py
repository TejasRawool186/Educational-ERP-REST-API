"""
Standardised error response builder.
"""
from datetime import datetime, timezone
from fastapi import HTTPException, status


def http_error(code: str, message: str, http_status: int) -> HTTPException:
    return HTTPException(
        status_code=http_status,
        detail={
            "error": {
                "code": code,
                "message": message,
                "status": http_status,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        },
    )


def not_found(resource: str = "Resource") -> HTTPException:
    return http_error("RESOURCE_NOT_FOUND", f"{resource} not found.", status.HTTP_404_NOT_FOUND)


def bad_request(message: str) -> HTTPException:
    return http_error("INVALID_PARAMETER", message, status.HTTP_400_BAD_REQUEST)


def db_error() -> HTTPException:
    return http_error(
        "DATABASE_ERROR",
        "A database error occurred. Please try again later.",
        status.HTTP_503_SERVICE_UNAVAILABLE,
    )
