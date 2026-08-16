import uuid

from fastapi import HTTPException, status

from app.models.employee import Employee
from app.repositories.department import DepartmentRepository
from app.repositories.employee import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeStatusUpdate, EmployeeUpdate


class EmployeeService:
    def __init__(
        self, employee_repo: EmployeeRepository, department_repo: DepartmentRepository
    ):
        self.employee_repo = employee_repo
        self.department_repo = department_repo

    def _generate_employee_code(self) -> str:
        # Simple unique code generator
        return f"EMP-{uuid.uuid4().hex[:8].upper()}"

    def get_employee(self, employee_id: int) -> Employee:
        employee = self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found",
            )
        return employee

    def get_employees(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[int, list[Employee]]:
        return self.employee_repo.get_list(skip=skip, limit=limit)

    def get_department_employees(
        self, department_id: int, skip: int = 0, limit: int = 100
    ) -> tuple[int, list[Employee]]:
        # Verify department exists
        department = self.department_repo.get_by_id(department_id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found",
            )
        return self.employee_repo.get_by_department(
            department_id, skip=skip, limit=limit
        )

    def search_employees(
        self, query: str, skip: int = 0, limit: int = 100
    ) -> tuple[int, list[Employee]]:
        return self.employee_repo.search(query, skip=skip, limit=limit)

    def create_employee(self, obj_in: EmployeeCreate) -> Employee:
        # Check for duplicate email
        existing = self.employee_repo.get_by_email(obj_in.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee with this email already exists",
            )

        # Verify department exists
        department = self.department_repo.get_by_id(obj_in.department_id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found",
            )

        employee_data = obj_in.model_dump()
        employee_data["employee_code"] = self._generate_employee_code()
        return self.employee_repo.create(**employee_data)

    def update_employee(self, employee_id: int, obj_in: EmployeeUpdate) -> Employee:
        employee = self.get_employee(employee_id)

        # Check duplicate email if email is being updated
        if obj_in.email and obj_in.email != employee.email:
            existing = self.employee_repo.get_by_email(obj_in.email)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Employee with this email already exists",
                )

        # Verify department if department is being updated
        if obj_in.department_id and obj_in.department_id != employee.department_id:
            department = self.department_repo.get_by_id(obj_in.department_id)
            if not department:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Department not found",
                )

        update_data = obj_in.model_dump(exclude_unset=True)
        return self.employee_repo.update(employee, update_data)

    def update_employee_status(
        self, employee_id: int, obj_in: EmployeeStatusUpdate
    ) -> Employee:
        employee = self.get_employee(employee_id)
        return self.employee_repo.update(employee, {"is_active": obj_in.is_active})

    def delete_employee(self, employee_id: int) -> None:
        employee = self.get_employee(employee_id)
        self.employee_repo.delete(employee.id)
