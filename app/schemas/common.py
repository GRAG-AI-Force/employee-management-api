from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    skip: int = Field(default=0, ge=0, description="Number of items to skip")
    limit: int = Field(
        default=100, ge=1, le=1000, description="Max number of items to return"
    )


class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    items: List[T]
    skip: int
    limit: int


class ErrorResponse(BaseModel):
    detail: str


class HealthResponse(BaseModel):
    status: str
    service: str
