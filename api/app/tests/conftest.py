
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, MagicMock
from app.models import Base, User
from app.helpers.database import get_db
from app.helpers.auth import get_authenticated_user

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
def mock_secrets_service():
    with patch('app.helpers.secrets_service.SecretsService', autospec=True) as mock:
        mock_instance = MagicMock()
        mock_instance.get_secret.return_value = "test-secret"
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture(scope="module")
def test_client(mock_secrets_service):
    # Set up
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authenticated_user] = lambda: {"sub": "test-user-123"}

    # Import app here to use the mock
    from app.main import app
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
