
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models import Base, User, DatadogAPIConfiguration
from app.helpers.database import get_db
from app.helpers.auth import get_authenticated_user

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def mock_auth_user():
    return {"sub": "test-user-123"}

@pytest.fixture(scope="module")
def test_client():
    # Set up
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authenticated_user] = mock_auth_user
    
    client = TestClient(app)
    
    # Create test user
    db = TestingSessionLocal()
    test_user = User(sub="test-user-123")
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    db.close()
    
    yield client
    
    # Tear down
    Base.metadata.drop_all(bind=engine)

def test_datadog_configuration_flow(test_client):
    # Test data
    config_data = {
        "app_key": "test-app-key-123",
        "api_key": "test-api-key-456"
    }
    
    # Create Datadog configuration
    response = test_client.post("/v1/datadog-configuration", json=config_data)
    assert response.status_code == 200
    assert "data" in response.json()
    assert "message" in response.json()["data"]
    assert response.json()["data"]["message"] == "Datadog API configuration created successfully"
    
    # Fetch vendor metrics using the configuration
    response = test_client.get("/v1/vendors-metrics/datadog")
    assert response.status_code in [200, 403]  # 403 is acceptable as keys are not real
    
    if response.status_code == 403:
        assert "error" in response.json()
        assert response.json()["error"] == "Authorization failed"
    
    # Try invalid configuration
    invalid_config = {
        "app_key": "",
        "api_key": ""
    }
    response = test_client.post("/v1/datadog-configuration", json=invalid_config)
    assert response.status_code == 400
