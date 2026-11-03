import pytest

from app_core import app, get_task_statistics


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_data(as_text=True) == "DevOps Midterm API is running!"
    assert response.mimetype == "text/plain"


def test_health(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_tasks(client):
    response = client.get("/api/tasks")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
    assert len(response.get_json()) == 3


def test_stats(client):
    response = client.get("/api/stats")

    assert response.status_code == 200
    assert response.get_json() == {
        "total": 3,
        "done": 1,
        "in_progress": 1,
        "pending": 1,
    }


@pytest.mark.parametrize(
    ("task_list", "expected"),
    [
        (
                [],
                {"total": 0, "done": 0, "in_progress": 0, "pending": 0},
        ),
        (
                [{"status": "done"}, {"status": "done"}],
                {"total": 2, "done": 2, "in_progress": 0, "pending": 0},
        ),
        (
                [
                    {"status": "done"},
                    {"status": "in_progress"},
                    {"status": "pending"},
                ],
                {"total": 3, "done": 1, "in_progress": 1, "pending": 1},
        ),
    ],
)
def test_task_statistics(task_list, expected):
    assert get_task_statistics(task_list) == expected


def test_unknown_endpoint_returns_404(client):
    response = client.get("/unknown")

    assert response.status_code == 404