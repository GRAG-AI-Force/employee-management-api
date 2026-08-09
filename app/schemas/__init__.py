from app.schemas.common import (
    ErrorResponse,
    HealthResponse,
    PaginatedResponse,
    PaginationParams,
)
from app.schemas.department import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
)
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeStatusUpdate,
    EmployeeUpdate,
)

__all__ = [
    "PaginationParams",
    "PaginatedResponse",
    "ErrorResponse",
    "HealthResponse",
    "DepartmentCreate",
    "DepartmentUpdate",
    "DepartmentResponse",
    "EmployeeCreate",
    "EmployeeUpdate",
    "EmployeeStatusUpdate",
    "EmployeeResponse",
]
