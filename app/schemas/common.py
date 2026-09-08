"""
Shared response envelope schemas used across all endpoints.
"""
from typing import Generic, TypeVar
from pydantic import BaseModel

DataT = TypeVar("DataT")


class PaginationMeta(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[DataT]):
    data: list[DataT]
    pagination: PaginationMeta


class SingleResponse(BaseModel, Generic[DataT]):
    data: DataT


class ErrorDetail(BaseModel):
    code: str
    message: str
    status: int
    timestamp: str | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail
