import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.fixture
def test_department(client: TestClient):
    response = client.post(
        "/api/v1/departments",
        json={"name": "Engineering-Test", "description": "Test dept"},
    )
    return response.json()


def test_create_employee(client: TestClient, test_department):
    dept_id = test_department["id"]
    response = client.post(
        "/api/v1/employees",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "job_title": "Developer",
            "salary": 80000.00,
            "department_id": dept_id,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["first_name"] == "John"
    assert data["email"] == "john.doe@example.com"
    assert "employee_code" in data
    assert data["is_active"] is True


def test_create_employee_invalid_salary(client: TestClient, test_department):
    response = client.post(
        "/api/v1/employees",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "job_title": "Developer",
            "salary": -100,  # Invalid salary
            "department_id": test_department["id"],
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_duplicate_email(client: TestClient, test_department):
    dept_id = test_department["id"]
    employee_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "job_title": "Designer",
        "salary": 70000.00,
        "department_id": dept_id,
    }
    # Create first
    client.post("/api/v1/employees", json=employee_data)
    # Try duplicate
    response = client.post("/api/v1/employees", json=employee_data)
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_employee_invalid_department(client: TestClient):
    response = client.post(
        "/api/v1/employees",
        json={
            "first_name": "Bob",
            "last_name": "Builder",
            "email": "bob@example.com",
            "job_title": "Builder",
            "salary": 50000.00,
            "department_id": 99999,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_employee(client: TestClient, test_department):
    create_res = client.post(
        "/api/v1/employees",
        json={
            "first_name": "Charlie",
            "last_name": "Brown",
            "email": "charlie@example.com",
            "job_title": "Manager",
            "salary": 90000.00,
            "department_id": test_department["id"],
        },
    )
    emp_id = create_res.json()["id"]

    response = client.get(f"/api/v1/employees/{emp_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "charlie@example.com"


def test_search_employees(client: TestClient, test_department):
    client.post(
        "/api/v1/employees",
        json={
            "first_name": "SearchFirst",
            "last_name": "SearchLast",
            "email": "search@example.com",
            "job_title": "Tester",
            "salary": 60000.00,
            "department_id": test_department["id"],
        },
    )

    response = client.get("/api/v1/employees/search?q=SearchFirst")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] >= 1
    assert data["items"][0]["first_name"] == "SearchFirst"


def test_update_employee_status(client: TestClient, test_department):
    create_res = client.post(
        "/api/v1/employees",
        json={
            "first_name": "Dave",
            "last_name": "Grohl",
            "email": "dave@example.com",
            "job_title": "Musician",
            "salary": 100000.00,
            "department_id": test_department["id"],
        },
    )
    emp_id = create_res.json()["id"]

    # Deactivate
    response = client.patch(
        f"/api/v1/employees/{emp_id}/status", json={"is_active": False}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["is_active"] is False


def test_delete_employee(client: TestClient, test_department):
    create_res = client.post(
        "/api/v1/employees",
        json={
            "first_name": "Eve",
            "last_name": "Adam",
            "email": "eve@example.com",
            "job_title": "Analyst",
            "salary": 75000.00,
            "department_id": test_department["id"],
        },
    )
    emp_id = create_res.json()["id"]

    response = client.delete(f"/api/v1/employees/{emp_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_res = client.get(f"/api/v1/employees/{emp_id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND


def test_employee_id_out_of_range(client: TestClient):
    # Out of 32-bit range (> 2_147_483_647)
    response = client.get("/api/v1/employees/26490016558")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Less than 1
    response = client.get("/api/v1/employees/0")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = client.get("/api/v1/employees/-5")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

