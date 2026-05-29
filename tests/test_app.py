"""Tests for the Activity Tracker API.

Some of these tests currently FAIL. That is expected -
the failures point to the bugs you need to fix.

Run with: pytest -v
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import storage


@pytest.fixture(autouse=True)
def reset_storage():
    storage.reset()
    yield
    storage.reset()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def user(client):
    response = client.post(
        "/users", json={"email": "alice@example.com", "name": "Alice"}
    )
    assert response.status_code == 201
    return response.json()


def test_health_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_user_returns_payload(client):
    response = client.post("/users", json={"email": "bob@example.com", "name": "Bob"})
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "bob@example.com"
    assert body["name"] == "Bob"
    assert "id" in body


def test_get_user_by_id(client, user):
    response = client.get(f"/users/{user['id']}")
    assert response.status_code == 200
    assert response.json()["email"] == user["email"]


def test_get_user_missing_returns_404(client):
    response = client.get("/users/9999")
    assert response.status_code == 404


def test_create_event_returns_201(client, user):
    response = client.post(
        "/events",
        json={"user_id": user["id"], "event_type": "login", "metadata": {}},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["event_type"] == "login"
    assert body["user_id"] == user["id"]


def test_create_event_with_unknown_user_returns_404(client):
    response = client.post(
        "/events",
        json={"user_id": 9999, "event_type": "login", "metadata": {}},
    )
    assert response.status_code == 404


def test_list_events_includes_created_items(client, user):
    for event_type in ["login", "page_view", "click", "page_view", "logout"]:
        client.post(
            "/events",
            json={"user_id": user["id"], "event_type": event_type, "metadata": {}},
        )

    response = client.get("/events?offset=0&limit=10")
    assert response.status_code == 200
    events = response.json()
    assert len(events) == 5


def test_list_events_paginates_without_overlap(client, user):
    for i in range(10):
        client.post(
            "/events",
            json={"user_id": user["id"], "event_type": "click", "metadata": {"i": i}},
        )

    page1 = client.get("/events?offset=0&limit=5").json()
    page2 = client.get("/events?offset=5&limit=5").json()

    assert len(page1) == 5
    assert len(page2) == 5
    page1_ids = {e["id"] for e in page1}
    page2_ids = {e["id"] for e in page2}
    assert page1_ids.isdisjoint(page2_ids), "Pages should not overlap"


def test_list_events_hides_soft_deleted_items(client, user):
    created_ids = []
    for _ in range(3):
        response = client.post(
            "/events",
            json={"user_id": user["id"], "event_type": "click", "metadata": {}},
        )
        created_ids.append(response.json()["id"])

    delete_response = client.delete(f"/events/{created_ids[1]}")
    assert delete_response.status_code == 204

    response = client.get("/events?offset=0&limit=10")
    assert response.status_code == 200
    remaining_ids = {e["id"] for e in response.json()}
    assert created_ids[1] not in remaining_ids
    assert len(response.json()) == 2


def test_delete_missing_event_returns_404(client):
    response = client.delete("/events/9999")
    assert response.status_code == 404


def test_delete_same_event_twice_changes_response(client, user):
    create_response = client.post(
        "/events",
        json={"user_id": user["id"], "event_type": "click", "metadata": {}},
    )
    event_id = create_response.json()["id"]

    first_delete = client.delete(f"/events/{event_id}")
    second_delete = client.delete(f"/events/{event_id}")

    assert first_delete.status_code == 204
    assert second_delete.status_code == 404


def test_pagination_after_delete_stays_consistent(client, user):
    created_ids = []
    for i in range(6):
        response = client.post(
            "/events",
            json={"user_id": user["id"], "event_type": "click", "metadata": {"i": i}},
        )
        created_ids.append(response.json()["id"])

    delete_response = client.delete(f"/events/{created_ids[2]}")
    assert delete_response.status_code == 204

    page1 = client.get("/events?offset=0&limit=3")
    page2 = client.get("/events?offset=3&limit=3")

    assert page1.status_code == 200
    assert page2.status_code == 200

    page1_ids = [event["id"] for event in page1.json()]
    page2_ids = [event["id"] for event in page2.json()]

    assert created_ids[2] not in page1_ids + page2_ids
    assert len(page1_ids) == 3
    assert len(page2_ids) == 2
    assert set(page1_ids).isdisjoint(page2_ids), "Pages should not overlap"
