"""
Tests for the Mergington High School Activities API
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


# ============= GET /activities Tests =============
def test_get_activities():
    """Test retrieving all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"


# ============= POST /activities/{activity_name}/signup Tests =============
def test_signup_for_activity_success():
    """Test successful signup for an activity"""
    email = "test_student@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"


def test_signup_for_activity_not_found():
    """Test signup for non-existent activity"""
    email = "test_student@mergington.edu"
    activity = "Nonexistent Activity"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_for_activity_already_signed_up():
    """Test signup for activity when already signed up"""
    email = "michael@mergington.edu"  # Already signed up for Chess Club
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


# ============= DELETE /activities/{activity_name}/signup Tests =============
def test_unregister_from_activity_success():
    """Test successful unregister from an activity"""
    email = "michael@mergington.edu"  # Already signed up for Chess Club
    activity = "Chess Club"
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"


def test_unregister_from_activity_not_found():
    """Test unregister from non-existent activity"""
    email = "test_student@mergington.edu"
    activity = "Nonexistent Activity"
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_not_signed_up():
    """Test unregister when student is not signed up"""
    email = "not_signed_up@mergington.edu"
    activity = "Chess Club"
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"