from fastapi.testclient import TestClient


def test_create_task(client: TestClient):
    response = client.post("/tasks/", json={
        "title": "Test task",
        "description": "Test description",
        "assignee": "Test assignee",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["status"] == "TODO"


def test_create_task_missing_field(client: TestClient):
    response = client.post("/tasks/", json={"title": "No assignee"})
    assert response.status_code == 422


def test_update_status(client: TestClient):
    created = client.post("/tasks/", json={
        "title": "Status test",
        "description": "description",
        "assignee": "Test assignee",
    }).json()
    task_id = created["id"]

    response = client.patch(f"/tasks/{task_id}", json={"status": "DONE"})
    assert response.status_code == 200
    assert response.json()["status"] == "DONE"


def test_status_rollback_from_done_forbidden(client: TestClient):
    created = client.post("/tasks/", json={
        "title": "Rollback test",
        "description": "description",
        "assignee": "Test assignee",
    }).json()
    task_id = created["id"]

    client.patch(f"/tasks/{task_id}", json={"status": "DONE"})

    response = client.patch(f"/tasks/{task_id}", json={"status": "TODO"})
    assert response.status_code == 400
    assert "DONE" in response.json()["message"]


def test_get_task_not_found(client: TestClient):
    response = client.get("/tasks/99999")
    assert response.status_code == 404

