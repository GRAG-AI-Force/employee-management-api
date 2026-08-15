from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    skip: int = Field(default=0, ge=0, description="Number of items to skip")
    limit: int = Field(
        default=100, ge=1, le=1000, description="Max number of items to return"
    )


class PaginatedResponse[T](BaseModel):
    total: int
    items: list[T]
    skip: int
    limit: int


class ErrorResponse(BaseModel):
    detail: str


class HealthResponse(BaseModel):
    status: str
    service: str
