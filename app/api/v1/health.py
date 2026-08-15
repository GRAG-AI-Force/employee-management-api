import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.dependencies.database import get_db
from app.schemas.common import HealthResponse

router = APIRouter(tags=["Health"])
logger = logging.getLogger(__name__)


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Liveness probe",
)
def health_check() -> HealthResponse:
    """
    Basic health check endpoint to verify the application is running.
    """
    return HealthResponse(status="healthy", service=settings.APP_NAME)


@router.get(
    "/ready",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Readiness probe",
)
def readiness_check(db: Session = Depends(get_db)) -> HealthResponse:
    """
    Readiness check endpoint that verifies connectivity to the database.
    """
    try:
        # Execute a simple query to ensure database is reachable
        db.execute(text("SELECT 1"))
        return HealthResponse(status="ready", service=settings.APP_NAME)
    except Exception as e:
        logger.error(f"Readiness check failed: {e!s}")
        # In a real scenario, returning 503 or 500 depends on orchestrator.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is not ready (Database connection failed)",
        ) from e
