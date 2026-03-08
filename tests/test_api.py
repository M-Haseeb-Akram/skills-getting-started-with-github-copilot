import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    original = activities.copy()
    yield
    activities.clear()
    activities.update(original)

def test_get_activities_success(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_success(client):
    response = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    assert "Signed up newstudent@mergington.edu for Chess Club" == response.json()["message"]
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]

def test_signup_activity_not_found(client):
    response = client.post("/activities/Nonexistent Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_signup_already_signed_up(client):
    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_delete_success(client):
    response = client.delete("/activities/Chess Club/signup?email=michael@mergington.edu")
    assert response.status_code == 200
    assert "Unregistered michael@mergington.edu from Chess Club" == response.json()["message"]
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]

def test_delete_activity_not_found(client):
    response = client.delete("/activities/Nonexistent Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_delete_not_signed_up(client):
    response = client.delete("/activities/Chess Club/signup?email=notsigned@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"