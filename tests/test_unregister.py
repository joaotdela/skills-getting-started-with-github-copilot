"""Tests for the unregister endpoint using AAA (Arrange-Act-Assert) pattern."""
from src.app import activities


class TestUnregisterSuccess:
    def test_unregister_existing_student_successfully(self, client):
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"  # Existing participant
        
        # Act
        response = client.post(f"/activities/{activity}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email not in activities[activity]["participants"]


class TestUnregisterNotRegistered:
    def test_unregister_not_registered_returns_400(self, client):
        # Arrange
        activity = "Chess Club"
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]


class TestUnregisterInvalidActivity:
    def test_unregister_nonexistent_activity_returns_404(self, client):
        # Arrange
        activity = "Fake Activity"
        email = "test@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestUnregisterParticipantsList:
    def test_unregister_removes_from_participants(self, client):
        # Arrange
        activity = "Programming Class"
        email = "emma@mergington.edu"
        original_count = len(activities[activity]["participants"])
        assert email in activities[activity]["participants"]
        
        # Act
        response = client.post(f"/activities/{activity}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert len(activities[activity]["participants"]) == original_count - 1
        assert email not in activities[activity]["participants"]


class TestUnregisterSignupUnregisterCycle:
    def test_signup_then_unregister_then_signup_again(self, client):
        # Arrange
        activity = "Tennis Club"
        email = "cyclist@mergington.edu"
        
        # Act & Assert - First signup
        signup_response = client.post(f"/activities/{activity}/signup?email={email}")
        assert signup_response.status_code == 200
        assert email in activities[activity]["participants"]
        
        # Act & Assert - Unregister
        unregister_response = client.post(f"/activities/{activity}/unregister?email={email}")
        assert unregister_response.status_code == 200
        assert email not in activities[activity]["participants"]
        
        # Act & Assert - Sign up again should succeed
        signup_again_response = client.post(f"/activities/{activity}/signup?email={email}")
        assert signup_again_response.status_code == 200
        assert email in activities[activity]["participants"]


class TestUnregisterResponseFormat:
    def test_unregister_response_contains_message(self, client):
        # Arrange
        activity = "Debate Club"
        email = "noah@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity}/unregister?email={email}")
        data = response.json()
        
        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]
