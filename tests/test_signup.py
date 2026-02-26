"""Tests for the signup endpoint using AAA (Arrange-Act-Assert) pattern."""
from src.app import activities


class TestSignupNewStudent:
    def test_signup_new_student_successfully(self, client):
        # Arrange
        activity = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in activities[activity]["participants"]


class TestSignupDuplicate:
    def test_signup_duplicate_email_returns_400(self, client):
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]


class TestSignupInvalidActivity:
    def test_signup_nonexistent_activity_returns_404(self, client):
        # Arrange
        activity = "Fake Activity"
        email = "test@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestSignupParticipantsList:
    def test_signup_adds_to_participants_list(self, client):
        # Arrange
        activity = "Programming Class"
        email = "alice@mergington.edu"
        original_count = len(activities[activity]["participants"])
        
        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert len(activities[activity]["participants"]) == original_count + 1
        assert activities[activity]["participants"][-1] == email


class TestSignupMultipleActivities:
    def test_signup_same_email_different_activities(self, client):
        # Arrange
        email = "student@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        
        # Act
        response1 = client.post(f"/activities/{activity1}/signup?email={email}")
        response2 = client.post(f"/activities/{activity2}/signup?email={email}")
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]


class TestSignupResponseFormat:
    def test_signup_response_contains_message(self, client):
        # Arrange
        activity = "Art Studio"
        email = "newuser@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")
        data = response.json()
        
        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]
