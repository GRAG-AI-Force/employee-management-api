# Employee Management API                                               
   
A production-ready FastAPI REST API for managing employees and departments. This application is designed to serve as a robust target for Jenkins CI/CD and DevSecOps pipelines.

## Project Overview

This API allows an organization to manage departments and their associated employees. It includes features like:
- Department CRUD and listing
- Employee CRUD, searching, filtering, and activation/deactivation
- Relational mapping between Employees and Departments
- Pagination for list endpoints  

## Architecture & Technology Stack

The application follows a layered modular architecture (Repository Pattern) for clean separation of concerns:
- **API Layer (`app/api/`)**: Route handlers and request/response validation.
- **Service Layer (`app/services/`)**: Business logic and validation.
- **Repository Layer (`app/repositories/`)**: Database queries and data access.
- **Models (`app/models/`)**: SQLAlchemy declarative models representing database tables.
- **Schemas (`app/schemas/`)**: Pydantic models for data validation and serialization.

### Technologies
- **Python 3.12**
- **FastAPI** + **Uvicorn**
- **Pydantic v2** + **Pydantic Settings**
- **SQLAlchemy 2.x** + **PostgreSQL** (`psycopg`)
- **Alembic** (Database Migrations)
- **Pytest** + **Pytest-Cov** (Testing)

## Project Structure

```text
.
├── app/
│   ├── api/          # FastAPI routers and endpoints
│   ├── core/         # Configuration, database setup, logging
│   ├── dependencies/ # FastAPI dependency injection (e.g., get_db)
│   ├── models/       # SQLAlchemy ORM models
│   ├── repositories/ # Data access logic
│   ├── schemas/      # Pydantic validation schemas
│   ├── services/     # Business logic
│   └── main.py       # FastAPI application entrypoint
├── alembic/          # Alembic database migration scripts
├── tests/            # Pytest test suite
├── Dockerfile        # Production multi-stage Docker build
├── .env.example      # Example environment variables
├── pyproject.toml    # Tooling config (Ruff, Black, isort, MyPy, Pytest)
├── requirements.txt  # Production dependencies
├── requirements-dev.txt # Development & testing dependencies
└── sonar-project.properties # SonarQube analysis configuration
```

## Local Setup

### 1. Create a Virtual Environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Environment Variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```
Ensure `DATABASE_URL` in `.env` points to your PostgreSQL instance. 
Example: `postgresql+psycopg://user:password@localhost:5432/employeedb`

### 4. Database Setup

Run the Alembic migrations to create the database tables:

```bash
alembic upgrade head
```

## Running the Application

Run the application locally using Uvicorn:

```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

## API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, visit:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## Health Checks

The application exposes two endpoints for orchestration and monitoring (e.g., AWS ECS, Kubernetes):
- Liveness Probe: `GET /api/v1/health`
- Readiness Probe: `GET /api/v1/ready` (Verifies database connectivity)

## Testing

The project uses `pytest` with an in-memory SQLite database for fast, isolated testing.

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=app --cov-report=term-missing --cov-report=xml
```

## Linting and Formatting

Configuration for all tools is centralized in `pyproject.toml`.

```bash
# Code Formatting
black .
isort .

# Linting
ruff check .

# Static Type Checking
mypy app/
```

## Docker

Build and run the application using the production-ready Dockerfile. It uses a multi-stage build, runs as a non-root user, and includes a health check.

```bash
# Build the image
docker build -t employee-management-api .

# Run the container (ensure DATABASE_URL is passed in)
docker run -p 8000:8000 -e DATABASE_URL="postgresql+psycopg://user:pass@host:5432/db" employee-management-api
```



this will work.


"Done"   "last final time" "oppp"    "done i guessss"
"super"  "opop"    "ok-done"     "op"    "webhook proeprly running"
"the public ip was the issue" "op"  "yes"  "great" "some changes" 
"lets go" "superman" "working properly now"  Last  "ok" "op"  "pop"  'op"  "kk"  "ok"  "kk"
"pop" "op"  "pop" "op"
"oop"  "pp" "pp"  '"pp"'  "ok"  "op" "pop"
