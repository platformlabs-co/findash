import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.helpers.auth import get_authenticated_user
from app.models import Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.helpers.database import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def test_client():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authenticated_user] = lambda: {"sub": "test-user-123"}

    client = TestClient(app)

    # Create test user
    db = TestingSessionLocal()
    test_user = User(sub="test-user-123", email="test@example.com")
    db.add(test_user)
    db.commit()
    db.close()

    yield client

    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides = {}


def test_get_vendor_metrics_invalid_vendor(test_client):
    response = test_client.get("/v1/vendors-metrics/invalid_vendor")
    assert response.status_code == 400
    assert response.json()["code"] == "INVALID_VENDOR"


def test_get_vendor_metrics_no_config(test_client):
    response = test_client.get("/v1/vendors-metrics/datadog")
    assert response.status_code == 404
    assert response.json()["code"] == "CONFIG_NOT_FOUND"
