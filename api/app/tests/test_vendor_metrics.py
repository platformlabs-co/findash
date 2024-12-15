import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.helpers.auth import get_authenticated_user


@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client


def mock_get_authenticated_user():
    return {"user_id": "test_user"}


def test_vendor_metrics_endpoint(test_client):
    app.dependency_overrides[get_authenticated_user] = mock_get_authenticated_user
    response = test_client.get("/v1/vendors-metrics")
    assert response.status_code == 200
    assert "data" in response.json()
    assert "message" in response.json()["data"]
    assert response.json()["data"]["message"] == "Welcome to the FinDash API"
    assert response.json()["data"]["user"] == {"user_id": "test_user"}
    app.dependency_overrides = {}
