"""HTTP integration tests using Flask's built-in test client."""

import pytest

from app import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    return app.test_client()


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"DevOps Calculator" in response.data


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_api_calculation(client):
    response = client.post("/api/calculate", json={"a": 10, "b": 2, "operation": "divide"})
    assert response.status_code == 200
    assert response.get_json()["result"] == 5


def test_api_rejects_division_by_zero(client):
    response = client.post("/api/calculate", json={"a": 10, "b": 0, "operation": "divide"})
    assert response.status_code == 400
    assert "zero" in response.get_json()["error"]
