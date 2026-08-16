from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field, field_serializer
NO_NULL_CHARS_PATTERN = r"^[^\x00]*$"


class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, pattern=NO_NULL_CHARS_PATTERN)
    description: str | None = Field(None, pattern=NO_NULL_CHARS_PATTERN)


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100, pattern=NO_NULL_CHARS_PATTERN)
    description: str | None = Field(None, pattern=NO_NULL_CHARS_PATTERN)


class DepartmentResponse(DepartmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at", when_used="json")
    def serialize_dt(self, dt: datetime) -> str:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt.isoformat()

    model_config = ConfigDict(from_attributes=True)
