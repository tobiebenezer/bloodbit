import json
from models.User.model import User
from database import db
import pytest

@pytest.fixture
def setup_user(client):
    """Create a user for testing login."""
    with client.application.app_context():
        user = User(name="testuser", email="test@example.com", blood_type="O+")
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()

def test_successful_login(client, setup_user):
    """Test a successful user login."""
    response = client.post("/auth/login", json={"email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "access_token" in data

def test_login_wrong_password(client, setup_user):
    """Test that login fails with an incorrect password."""
    response = client.post("/auth/login", json={"email": "test@example.com", "password": "wrongpassword"})
    assert response.status_code == 401

def test_login_wrong_email(client, setup_user):
    """Test that login fails with a nonexistent email."""
    response = client.post("/auth/login", json={"email": "wrong@example.com", "password": "testpassword"})
    assert response.status_code == 401

def test_login_no_json(client):
    """Test that login fails without a JSON body."""
    response = client.post("/auth/login")
    assert response.status_code == 415
