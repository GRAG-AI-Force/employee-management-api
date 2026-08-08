from fastapi import APIRouter

from app.api.v1.departments import router as departments_router
from app.api.v1.employees import router as employees_router
from app.api.v1.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(departments_router)
api_router.include_router(employees_router)
