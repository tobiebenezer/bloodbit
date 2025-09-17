import json
from models.User.model import User
from models.Donor.model import Donor
from database import db
import pytest

# Helper function to create a user and get a token
def get_auth_token(client, email, password, name="Test User", blood_type="O+"):
    with client.application.app_context():
        user = User(name=name, email=email, blood_type=blood_type)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user.id
    
@pytest.fixture
def user1_token(client):
    with client.application.app_context():
        user = User(name="User One", email="user1@test.com", blood_type="A+")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    response = client.post("/auth/login", json={"email": "user1@test.com", "password": "password123"})
    return json.loads(response.data)["access_token"]

@pytest.fixture
def user2_token(client):
    with client.application.app_context():
        user = User(name="User Two", email="user2@test.com", blood_type="B-")
        user.set_password("password456")
        db.session.add(user)
        db.session.commit()

    response = client.post("/auth/login", json={"email": "user2@test.com", "password": "password456"})
    return json.loads(response.data)["access_token"]

def test_create_donor_profile(client, user1_token):
    """
    Test creating a new donor profile.
    """
    response = client.post(
        "/donors/",
        headers={"Authorization": f"Bearer {user1_token}"},
        json={"medical_history": "Healthy", "is_available": True, "blood_type": "A+"}
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["medical_history"] == "Healthy"
    assert data["is_available"] is True
    assert "created_at" in data
    assert "updated_at" in data

def test_get_all_donors(client, user1_token):
    """
    Test retrieving all donor profiles.
    """
    client.post(
        "/donors/",
        headers={"Authorization": f"Bearer {user1_token}"},
        json={"medical_history": "Some history", "is_available": False, "blood_type": "A+"}
    )

    response = client.get("/donors/", headers={"Authorization": f"Bearer {user1_token}"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_specific_donor(client, user1_token):
    """
    Test retrieving a single donor profile.
    """
    post_response = client.post(
        "/donors/",
        headers={"Authorization": f"Bearer {user1_token}"},
        json={"medical_history": "Specific donor history", "is_available": True, "blood_type": "O-"}
    )
    donor_id = json.loads(post_response.data)["id"]

    response = client.get(f"/donors/{donor_id}", headers={"Authorization": f"Bearer {user1_token}"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == donor_id
    assert data["medical_history"] == "Specific donor history"

def test_update_donor_profile(client, user1_token):
    """
    Test updating a donor's own profile.
    """
    post_response = client.post(
        "/donors/",
        headers={"Authorization": f"Bearer {user1_token}"},
        json={"medical_history": "Initial history", "is_available": True, "blood_type": "B+"}
    )
    donor_id = json.loads(post_response.data)["id"]

    response = client.put(
        f"/donors/{donor_id}",
        headers={"Authorization": f"Bearer {user1_token}"},
        json={"is_available": False}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["is_available"] is False

def test_unauthorized_update(client, user1_token, user2_token):
    """
    Test that a user cannot update another user's donor profile.
    """
    post_response = client.post(
        "/donors/",
        headers={"Authorization": f"Bearer {user1_token}"},
        json={"medical_history": "User 1 history", "is_available": True, "blood_type": "A+"}
    )
    donor_id = json.loads(post_response.data)["id"]

    # Attempt to update with user2's token
    response = client.put(
        f"/donors/{donor_id}",
        headers={"Authorization": f"Bearer {user2_token}"},
        json={"is_available": False}
    )
    assert response.status_code == 401
