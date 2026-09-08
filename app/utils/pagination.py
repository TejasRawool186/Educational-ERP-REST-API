"""
Pagination helpers.
"""
from fastapi import Query
from app.core.config import settings
from app.schemas.common import PaginationMeta


class PaginationParams:
    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Page number (1-based)"),
        limit: int = Query(
            default=settings.DEFAULT_PAGE_SIZE,
            ge=1,
            le=settings.MAX_PAGE_SIZE,
            description="Records per page (max 1000)",
        ),
    ):
        self.page = page
        self.limit = limit

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


def make_pagination_meta(page: int, limit: int, total: int) -> PaginationMeta:
    import math
    return PaginationMeta(
        page=page,
        limit=limit,
        total=total,
        total_pages=math.ceil(total / limit) if limit else 0,
    )
