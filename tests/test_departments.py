from fastapi import status
from fastapi.testclient import TestClient


def test_create_department(client: TestClient):
    response = client.post(
        "/api/v1/departments",
        json={"name": "Engineering", "description": "Tech department"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Engineering"
    assert "id" in data


def test_create_duplicate_department(client: TestClient):
    # Create first
    client.post("/api/v1/departments", json={"name": "HR"})
    # Try duplicate
    response = client.post("/api/v1/departments", json={"name": "HR"})
    assert response.status_code == status.HTTP_409_CONFLICT


def test_get_department(client: TestClient):
    create_res = client.post("/api/v1/departments", json={"name": "Sales"})
    dept_id = create_res.json()["id"]

    response = client.get(f"/api/v1/departments/{dept_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Sales"


def test_get_nonexistent_department(client: TestClient):
    response = client.get("/api/v1/departments/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_departments(client: TestClient):
    client.post("/api/v1/departments", json={"name": "Marketing"})
    client.post("/api/v1/departments", json={"name": "Finance"})

    response = client.get("/api/v1/departments")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert len(data["items"]) >= 2


def test_update_department(client: TestClient):
    create_res = client.post("/api/v1/departments", json={"name": "Support"})
    dept_id = create_res.json()["id"]

    response = client.put(
        f"/api/v1/departments/{dept_id}",
        json={"name": "Customer Support", "description": "Updated"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Customer Support"
    assert data["description"] == "Updated"


def test_delete_department(client: TestClient):
    create_res = client.post("/api/v1/departments", json={"name": "Legal"})
    dept_id = create_res.json()["id"]

    response = client.delete(f"/api/v1/departments/{dept_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify deletion
    get_res = client.get(f"/api/v1/departments/{dept_id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND


def test_department_id_out_of_range(client: TestClient):
    # Out of 32-bit range (> 2_147_483_647)
    response = client.get("/api/v1/departments/26490016558")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Less than 1
    response = client.get("/api/v1/departments/0")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = client.get("/api/v1/departments/-10")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
