from fastapi import HTTPException, status

from app.models.department import Department
from app.repositories.department import DepartmentRepository
from app.schemas.department import DepartmentCreate, DepartmentUpdate


class DepartmentService:
    def __init__(self, repository: DepartmentRepository):
        self.repository = repository

    def get_department(self, department_id: int) -> Department:
        department = self.repository.get_by_id(department_id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found",
            )
        return department

    def get_departments(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[int, list[Department]]:
        return self.repository.get_list(skip=skip, limit=limit)

    def create_department(self, obj_in: DepartmentCreate) -> Department:
        # Check for duplicate name
        existing = self.repository.get_by_name(obj_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Department with this name already exists",
            )
        return self.repository.create(obj_in)

    def update_department(
        self, department_id: int, obj_in: DepartmentUpdate
    ) -> Department:
        department = self.get_department(department_id)

        # Check duplicate name if name is being updated
        if obj_in.name and obj_in.name != department.name:
            existing = self.repository.get_by_name(obj_in.name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Department with this name already exists",
                )

        return self.repository.update(department, obj_in)

    def delete_department(self, department_id: int) -> None:
        department = self.get_department(department_id)
        # Note: if there are employees, cascade="all, delete-orphan" will
        # delete them.
        self.repository.delete(department.id)
