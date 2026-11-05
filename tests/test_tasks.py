import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("TASKBOARD_DB", str(tmp_path / "test.db"))
    from app.main import app
    return TestClient(app)


def test_create_and_list(client):
    r = client.post("/api/tasks", json={"title": "Comprar leche"})
    assert r.status_code == 201
    data = client.get("/api/tasks?page=0").json()
    assert any(t["title"] == "Comprar leche" for t in data["items"])


def test_toggle(client):
    task = client.post("/api/tasks", json={"title": "X"}).json()
    r = client.patch(f"/api/tasks/{task['id']}/toggle")
    assert r.json()["status"] == "done"


def test_delete(client):
    task = client.post("/api/tasks", json={"title": "X"}).json()
    assert client.delete(f"/api/tasks/{task['id']}").status_code == 204
    assert client.delete(f"/api/tasks/{task['id']}").status_code == 404
