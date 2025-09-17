import json
from models.User.model import User
from database import db
import pytest

# Helper function to create a user and get a token
def get_auth_token(client, email, password, name="Test User", blood_type="O+"):
    with client.application.app_context():
        user = User(name=name, email=email, blood_type=blood_type)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
    
    response = client.post("/auth/login", json={"email": email, "password": password})
    return json.loads(response.data)["access_token"]

@pytest.fixture
def requester_token(client):
    return get_auth_token(client, "requester@test.com", "password123", name="Requester", blood_type="A-")

@pytest.fixture
def donor_token(client):
    return get_auth_token(client, "donor@test.com", "password456", name="Donor", blood_type="B+")

def test_create_blood_request(client, requester_token):
    """
    Test creating a new blood request.
    """
    response = client.post(
        "/blood-requests/",
        headers={"Authorization": f"Bearer {requester_token}"},
        json={
            "name": "John Doe",
            "phone": "123-456-7890",
            "blood_type": "A-",
            "quantity": 2,
            "location": "Central Hospital"
        }
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["name"] == "John Doe"
    assert data["phone"] == "123-456-7890"
    assert data["blood_type"] == "A-"
    assert data["status"] == "Pending"
    assert "created_at" in data
    assert "updated_at" in data

def test_get_all_blood_requests(client, requester_token):
    """
    Test retrieving all blood requests.
    """
    # Create a request first
    client.post(
        "/blood-requests/",
        headers={"Authorization": f"Bearer {requester_token}"},
        json={"name": "Jane Doe", "phone": "555-5555", "blood_type": "O+", "quantity": 1, "location": "City Clinic"}
    )
    
    response = client.get("/blood-requests/", headers={"Authorization": f"Bearer {requester_token}"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Jane Doe"

def test_get_specific_blood_request(client, requester_token):
    """
    Test retrieving a single blood request by its ID.
    """
    post_response = client.post(
        "/blood-requests/",
        headers={"Authorization": f"Bearer {requester_token}"},
        json={"name": "Specific Case", "phone": "987-654-3210", "blood_type": "AB+", "quantity": 3, "location": "Regional Medical Center"}
    )
    request_id = json.loads(post_response.data)["id"]

    response = client.get(f"/blood-requests/{request_id}", headers={"Authorization": f"Bearer {requester_token}"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["name"] == "Specific Case"
    assert data["id"] == request_id

def test_update_blood_request_status(client, requester_token):
    """
    Test updating the status of a blood request.
    """
    post_response = client.post(
        "/blood-requests/",
        headers={"Authorization": f"Bearer {requester_token}"},
        json={"name": "Update Status", "phone": "111-222-3333", "blood_type": "B-", "quantity": 1, "location": "Downtown Hospital"}
    )
    request_id = json.loads(post_response.data)["id"]
    original_updated_at = json.loads(post_response.data)["updated_at"]

    response = client.put(
        f"/blood-requests/{request_id}",
        headers={"Authorization": f"Bearer {requester_token}"},
        json={"status": "Fulfilled"}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "Fulfilled"
    assert data["updated_at"] > original_updated_at

def test_update_blood_request_unauthorized(client, requester_token, donor_token):
    """
    Test that a user cannot update a blood request they did not create.
    """
    post_response = client.post(
        "/blood-requests/",
        headers={"Authorization": f"Bearer {requester_token}"},
        json={"name": "Unauthorized Test", "phone": "444-555-6666", "blood_type": "A+", "quantity": 1, "location": "Suburban Hospital"}
    )
    request_id = json.loads(post_response.data)["id"]
    
    # Try to update with another user's token
    response = client.put(
        f"/blood-requests/{request_id}",
        headers={"Authorization": f"Bearer {donor_token}"},
        json={"status": "Cancelled"}
    )
    assert response.status_code == 401

def test_get_nonexistent_request(client, requester_token):
    """
    Test that fetching a nonexistent blood request returns a 404 error.
    """
    response = client.get("/blood-requests/9999", headers={"Authorization": f"Bearer {requester_token}"})
    assert response.status_code == 404
