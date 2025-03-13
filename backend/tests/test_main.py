from fastapi.testclient import TestClient
from app.main import app


def test_read_root():
    """Test the root endpoint."""
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the Math LMS API"}