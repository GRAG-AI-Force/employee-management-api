from typing import Any

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.employee import Employee


class EmployeeRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, employee_id: int) -> Employee | None:
        return self.session.get(Employee, employee_id)

    def get_by_email(self, email: str) -> Employee | None:
        stmt = select(Employee).where(Employee.email == email)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_list(self, skip: int = 0, limit: int = 100) -> tuple[int, list[Employee]]:
        count_stmt = select(func.count()).select_from(Employee)
        total = self.session.execute(count_stmt).scalar_one()

        stmt = select(Employee).offset(skip).limit(limit).order_by(Employee.id)
        items = list(self.session.execute(stmt).scalars().all())

        return total, items

    def get_by_department(
        self, department_id: int, skip: int = 0, limit: int = 100
    ) -> tuple[int, list[Employee]]:
        count_stmt = (
            select(func.count())
            .select_from(Employee)
            .where(Employee.department_id == department_id)
        )
        total = self.session.execute(count_stmt).scalar_one()

        stmt = (
            select(Employee)
            .where(Employee.department_id == department_id)
            .offset(skip)
            .limit(limit)
            .order_by(Employee.id)
        )
        items = list(self.session.execute(stmt).scalars().all())

        return total, items

    def search(
        self, query: str, skip: int = 0, limit: int = 100
    ) -> tuple[int, list[Employee]]:
        search_filter = or_(
            Employee.first_name.ilike(f"%{query}%"),
            Employee.last_name.ilike(f"%{query}%"),
            Employee.email.ilike(f"%{query}%"),
            Employee.employee_code.ilike(f"%{query}%"),
        )

        count_stmt = select(func.count()).select_from(Employee).where(search_filter)
        total = self.session.execute(count_stmt).scalar_one()

        stmt = (
            select(Employee)
            .where(search_filter)
            .offset(skip)
            .limit(limit)
            .order_by(Employee.id)
        )
        items = list(self.session.execute(stmt).scalars().all())

        return total, items

    def create(self, **kwargs: Any) -> Employee:
        db_obj = Employee(**kwargs)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def update(self, db_obj: Employee, update_data: dict) -> Employee:
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def delete(self, employee_id: int) -> None:
        db_obj = self.get_by_id(employee_id)
        if db_obj:
            self.session.delete(db_obj)
            self.session.commit()
