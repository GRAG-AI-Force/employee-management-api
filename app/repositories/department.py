from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate


class DepartmentRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, department_id: int) -> Department | None:
        return self.session.get(Department, department_id)

    def get_by_name(self, name: str) -> Department | None:
        stmt = select(Department).where(Department.name == name)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_list(self, skip: int = 0, limit: int = 100) -> tuple[int, list[Department]]:
        # Count
        count_stmt = select(func.count()).select_from(Department)
        total = self.session.execute(count_stmt).scalar_one()

        # Data
        stmt = select(Department).offset(skip).limit(limit).order_by(Department.id)
        items = list(self.session.execute(stmt).scalars().all())

        return total, items

    def create(self, obj_in: DepartmentCreate) -> Department:
        db_obj = Department(**obj_in.model_dump())
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def update(self, db_obj: Department, obj_in: DepartmentUpdate) -> Department:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def delete(self, department_id: int) -> None:
        db_obj = self.get_by_id(department_id)
        if db_obj:
            self.session.delete(db_obj)
            self.session.commit()
