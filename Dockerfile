# Stage 1: Build environment
FROM python:3.12-slim as builder

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Runtime environment
FROM python:3.12-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends libpq5 curl && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -s /bin/bash -m appuser

WORKDIR /app

# Copy wheels and install
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy application code
COPY --chown=appuser:appgroup ./app /app/app
COPY --chown=appuser:appgroup ./alembic /app/alembic
COPY --chown=appuser:appgroup ./alembic.ini /app/alembic.ini

# Set ownership and switch to non-root user
RUN chown -R appuser:appgroup /app
USER appuser

ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production

# Expose the application port
EXPOSE 8000

# Healthcheck for ECS / Docker
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
