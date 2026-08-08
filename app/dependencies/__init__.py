from app.dependencies.database import get_db
from app.dependencies.services import get_department_service, get_employee_service

__all__ = ["get_db", "get_department_service", "get_employee_service"]
