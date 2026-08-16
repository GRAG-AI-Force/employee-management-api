from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status

from app.dependencies.query import strict_query_params
from app.dependencies.services import get_department_service, get_employee_service
from app.schemas.common import ErrorResponse, PaginatedResponse
from app.schemas.department import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
)
from app.schemas.employee import EmployeeResponse
from app.services.department import DepartmentService
from app.services.employee import EmployeeService

router = APIRouter(prefix="/departments", tags=["Departments"])

DepartmentId = Annotated[
    int,
    Path(
        ge=1,
        le=2_147_483_647,
        description="Department ID (32-bit integer)",
    ),
]


@router.post(
    "",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Bad Request",
        },
        status.HTTP_409_CONFLICT: {"model": ErrorResponse, "description": "Conflict"},
    },
    summary="Create a new department",
)
def create_department(
    department: DepartmentCreate,
    service: DepartmentService = Depends(get_department_service),
) -> DepartmentResponse:
    return service.create_department(department)  # type: ignore


@router.get(
    "",
    response_model=PaginatedResponse[DepartmentResponse],
    summary="List departments",
    dependencies=[Depends(strict_query_params({"skip", "limit"}))],
)
def list_departments(
    skip: int = Query(0, ge=0, le=100_000),
    limit: int = Query(100, ge=1, le=100),
    service: DepartmentService = Depends(get_department_service),
) -> dict:
    total, items = service.get_departments(skip=skip, limit=limit)
    return {"total": total, "items": items, "skip": skip, "limit": limit}


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Not Found"},
    },
    summary="Get a department by ID",
)
def get_department(
    department_id: DepartmentId,
    service: DepartmentService = Depends(get_department_service),
) -> DepartmentResponse:
    return service.get_department(department_id)  # type: ignore


@router.put(
    "/{department_id}",
    response_model=DepartmentResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Bad Request",
        },
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Not Found"},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse, "description": "Conflict"},
    },
    summary="Update a department",
)
def update_department(
    department_id: DepartmentId,
    department: DepartmentUpdate,
    service: DepartmentService = Depends(get_department_service),
) -> DepartmentResponse:
    return service.update_department(department_id, department)  # type: ignore


@router.delete(
    "/{department_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Not Found"},
    },
    summary="Delete a department",
)
def delete_department(
    department_id: DepartmentId,
    service: DepartmentService = Depends(get_department_service),
) -> None:
    service.delete_department(department_id)


@router.get(
    "/{department_id}/employees",
    response_model=PaginatedResponse[EmployeeResponse],
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Not Found"},
    },
    summary="List employees in a department",
    dependencies=[Depends(strict_query_params({"skip", "limit"}))],
)
def list_department_employees(
    department_id: DepartmentId,
    skip: int = Query(0, ge=0, le=100_000),
    limit: int = Query(100, ge=1, le=100),
    service: EmployeeService = Depends(get_employee_service),
) -> dict:
    total, items = service.get_department_employees(
        department_id, skip=skip, limit=limit
    )
    return {"total": total, "items": items, "skip": skip, "limit": limit}
