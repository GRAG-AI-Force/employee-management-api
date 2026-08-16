import re
from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_serializer,
    field_validator,
)
from pydantic.json_schema import WithJsonSchema

StrictDecimal = Annotated[
    Decimal,
    WithJsonSchema(
        {
            "type": "number",
            "format": "decimal",
            "minimum": 0.01,
            "maximum": 99999999.99,
        }
    ),
]


class EmployeeBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=100, pattern=r"^[^\x00]*$")
    last_name: str = Field(..., min_length=2, max_length=100, pattern=r"^[^\x00]*$")
    email: EmailStr
    phone: str | None = Field(None, max_length=20, pattern=r"^[\d\+\-\s\(\)]+$")
    job_title: str = Field(..., min_length=2, max_length=100, pattern=r"^[^\x00]*$")
    salary: StrictDecimal = Field(
        ...,
        ge=Decimal("0.01"),
        le=Decimal("99999999.99"),
    )
    department_id: int = Field(..., ge=1, le=2_147_483_647)
    is_active: bool = True

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        if v == "" or v is None:
            return None
        if not re.match(r"^[\d\+\-\s\(\)]+$", v):
            raise ValueError("Invalid phone number format")
        return v


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    first_name: str | None = Field(
        None, min_length=2, max_length=100, pattern=r"^[^\x00]*$"
    )
    last_name: str | None = Field(
        None, min_length=2, max_length=100, pattern=r"^[^\x00]*$"
    )
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=20, pattern=r"^[\d\+\-\s\(\)]+$")
    job_title: str | None = Field(
        None, min_length=2, max_length=100, pattern=r"^[^\x00]*$"
    )
    salary: StrictDecimal | None = Field(
        None,
        ge=Decimal("0.01"),
        le=Decimal("99999999.99"),
    )
    department_id: int | None = Field(None, ge=1, le=2_147_483_647)
    is_active: bool | None = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        if v == "" or v is None:
            return None
        if not re.match(r"^[\d\+\-\s\(\)]+$", v):
            raise ValueError("Invalid phone number format")
        return v


class EmployeeStatusUpdate(BaseModel):
    is_active: bool


class EmployeeResponse(EmployeeBase):
    id: int
    employee_code: str
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at", when_used="json")
    def serialize_dt(self, dt: datetime) -> str:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt.isoformat()

    model_config = ConfigDict(from_attributes=True)
