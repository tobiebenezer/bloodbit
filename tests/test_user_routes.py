import json
from models.User.model import User
from database import db
import pytest

@pytest.fixture
def auth_token(client):
    """Create a user and return an auth token."""
    with client.application.app_context():
        user = User(name="testuser", email="test@example.com", blood_type="O+", location="Test City")
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()

    response = client.post("/auth/login", json={"email": "test@example.com", "password": "testpassword"})
    return json.loads(response.data)["access_token"]

def test_create_user(client):
    """Test creating a new user."""
    response = client.post("/users/", json={
        "name": "newuser",
        "email": "new@example.com",
        "password": "newpassword",
        "blood_type": "A-",
        "location": "New City"
    })
    assert response.status_code == 201
    assert json.loads(response.data)["message"] == "User registered successfully"

def test_get_all_users(client, auth_token):
    """Test retrieving all users."""
    response = client.get("/users/", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    # At least the user from the fixture should exist
    assert len(data) >= 1
    assert data[0]["email"] == "test@example.com"

def test_get_specific_user(client, auth_token):
    """Test retrieving a specific user by ID with a valid token."""
    with client.application.app_context():
        user_id = User.query.filter_by(email="test@example.com").first().id
    
    response = client.get(f"/users/{user_id}", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["email"] == "test@example.com"
    assert data["name"] == "testuser"
    assert data["location"] == "Test City"

def test_get_user_unauthorized(client):
    """Test that getting a user without a token fails."""
    # Assumes a user with ID 1 exists or is created by other tests
    response = client.get("/users/1")
    assert response.status_code == 401

def test_get_user_invalid_token(client):
    """Test that getting a user with an invalid token fails."""
    response = client.get("/users/1", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 422

def test_get_nonexistent_user(client, auth_token):
    """Test retrieving a nonexistent user returns 404."""
    response = client.get("/users/9999", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 404
