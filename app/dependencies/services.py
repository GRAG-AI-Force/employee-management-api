from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.repositories.department import DepartmentRepository
from app.repositories.employee import EmployeeRepository
from app.services.department import DepartmentService
from app.services.employee import EmployeeService


def get_department_service(db: Session = Depends(get_db)) -> DepartmentService:  # noqa: B008
    repository = DepartmentRepository(db)
    return DepartmentService(repository)


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:  # noqa: B008
    employee_repo = EmployeeRepository(db)
    department_repo = DepartmentRepository(db)
    return EmployeeService(employee_repo, department_repo)
