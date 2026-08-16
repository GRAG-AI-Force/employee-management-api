from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status

from app.dependencies.services import get_employee_service
from app.dependencies.query import strict_query_params
from app.schemas.common import ErrorResponse, PaginatedResponse
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeStatusUpdate,
    EmployeeUpdate,
)
from app.services.employee import EmployeeService

router = APIRouter(prefix="/employees", tags=["Employees"])

EmployeeId = Annotated[
    int,
    Path(
        ge=1,
        le=2_147_483_647,
        description="Employee ID (32-bit integer)",
    ),
]


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Bad Request",
        },
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Department not found"},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse, "description": "Conflict"},
    },
    summary="Create a new employee",
)
def create_employee(
    employee: EmployeeCreate,
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeResponse:
    return service.create_employee(employee)  # type: ignore


@router.get(
    "/search",
    response_model=PaginatedResponse[EmployeeResponse],
    summary="Search employees by name, email, or code",
    dependencies=[Depends(strict_query_params({"q", "skip", "limit"}))],
)
def search_employees(
    q: str = Query(..., min_length=2, pattern=r"^[^\x00]*$", description="Search term"),
    skip: int = Query(0, ge=0, le=100_000),
    limit: int = Query(100, ge=1, le=100),
    service: EmployeeService = Depends(get_employee_service),
) -> dict:
    total, items = service.search_employees(q, skip=skip, limit=limit)
    return {"total": total, "items": items, "skip": skip, "limit": limit}


@router.get(
    "",
    response_model=PaginatedResponse[EmployeeResponse],
    summary="List all employees",
    dependencies=[Depends(strict_query_params({"skip", "limit"}))],
)
def list_employees(
    skip: int = Query(0, ge=0, le=100_000),
    limit: int = Query(100, ge=1, le=100),
    service: EmployeeService = Depends(get_employee_service),
) -> dict:
    total, items = service.get_employees(skip=skip, limit=limit)
    return {"total": total, "items": items, "skip": skip, "limit": limit}


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Not Found"},
    },
    summary="Get an employee by ID",
)
def get_employee(
    employee_id: EmployeeId,
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeResponse:
    return service.get_employee(employee_id)  # type: ignore


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Bad Request",
        },
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Not Found"},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse, "description": "Conflict"},
    },
    summary="Update an employee",
)
def update_employee(
    employee_id: EmployeeId,
    employee: EmployeeUpdate,
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeResponse:
    return service.update_employee(employee_id, employee)  # type: ignore


@router.patch(
    "/{employee_id}/status",
    response_model=EmployeeResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Bad Request",
        },
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Not Found"},
    },
    summary="Update employee active status",
)
def update_employee_status(
    employee_id: EmployeeId,
    status_update: EmployeeStatusUpdate,
    service: EmployeeService = Depends(get_employee_service),
) -> EmployeeResponse:
    return service.update_employee_status(employee_id, status_update)  # type: ignore


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Not Found"},
    },
    summary="Delete an employee",
)
def delete_employee(
    employee_id: EmployeeId,
    service: EmployeeService = Depends(get_employee_service),
) -> None:
    service.delete_employee(employee_id)
