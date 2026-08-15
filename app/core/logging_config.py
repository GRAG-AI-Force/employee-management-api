import logging
import sys
from datetime import UTC, datetime
from typing import Any

from app.core.config import settings


class JsonFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.
    """

    def format(self, record: logging.LogRecord) -> str:
        # Standard fields
        log_obj: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=UTC
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Include contextual fields if they exist
        if hasattr(record, "request_id"):
            log_obj["request_id"] = record.request_id
        if hasattr(record, "request_method"):
            log_obj["request_method"] = record.request_method
        if hasattr(record, "endpoint"):
            log_obj["endpoint"] = record.endpoint
        if hasattr(record, "status_code"):
            log_obj["status_code"] = record.status_code

        # Add exception traceback if present
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        import json

        return json.dumps(log_obj)


def setup_logging() -> None:
    """Configure application logging."""
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)

    # Clear existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Stream handler for stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(JsonFormatter())
    logger.addHandler(stream_handler)

    # Configure uvicorn loggers to use our formatter
    for uvicorn_logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error"):
        uvicorn_logger = logging.getLogger(uvicorn_logger_name)
        uvicorn_logger.handlers = [stream_handler]
        uvicorn_logger.propagate = False
