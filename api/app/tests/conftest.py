
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, MagicMock
from app.models import Base, User
from app.helpers.database import get_db
from app.helpers.auth import get_authenticated_user
from app.helpers.config import Config

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def test_client():
    # Mock Config
    mock_config = MagicMock(spec=Config)
    mock_config.AppSecretKey = "test-secret-key"
    mock_config.Auth0Domain = "test.auth0.com"
    mock_config.Auth0Audience = "test-audience"
    
    with patch('app.helpers.config.Config', return_value=mock_config):
        from app.main import app

        Base.metadata.create_all(bind=engine)
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_authenticated_user] = lambda: {"sub": "test-user-123"}

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
