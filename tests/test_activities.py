"""Tests for the activities endpoint using AAA (Arrange-Act-Assert) pattern."""
from src.app import activities


class TestGetActivitiesSuccess:
    def test_get_activities_returns_all_activities(self, client):
        # Arrange (implicit - activities fixture already populated)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9
        assert "Chess Club" in data
        assert "Programming Class" in data


class TestGetActivitiesContent:
    def test_get_activities_includes_participants(self, client):
        # Arrange
        
        # Act
        response = client.get("/activities")
        
        # Assert
        data = response.json()
        assert "participants" in data["Chess Club"]
        assert isinstance(data["Chess Club"]["participants"], list)
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]


class TestGetActivitiesStructure:
    def test_get_activities_has_correct_structure(self, client):
        # Arrange
        expected_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        
        # Assert
        data = response.json()
        for activity_name, activity_data in data.items():
            assert set(activity_data.keys()) == expected_fields


class TestGetActivitiesFields:
    def test_get_activities_has_valid_descriptions(self, client):
        # Arrange
        
        # Act
        response = client.get("/activities")
        
        # Assert
        data = response.json()
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["description"], str)
            assert len(activity_data["description"]) > 0


    def test_get_activities_has_valid_schedules(self, client):
        # Arrange
        
        # Act
        response = client.get("/activities")
        
        # Assert
        data = response.json()
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["schedule"], str)
            assert len(activity_data["schedule"]) > 0


    def test_get_activities_has_valid_max_participants(self, client):
        # Arrange
        
        # Act
        response = client.get("/activities")
        
        # Assert
        data = response.json()
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["max_participants"], int)
            assert activity_data["max_participants"] > 0


class TestGetActivitiesInitialState:
    def test_chess_club_initial_participants(self, client):
        # Arrange
        expected_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
        
        # Act
        response = client.get("/activities")
        
        # Assert
        data = response.json()
        assert data["Chess Club"]["participants"] == expected_participants


    def test_programming_class_initial_participants(self, client):
        # Arrange
        expected_participants = ["emma@mergington.edu", "sophia@mergington.edu"]
        
        # Act
        response = client.get("/activities")
        
        # Assert
        data = response.json()
        assert data["Programming Class"]["participants"] == expected_participants


class TestGetActivitiesAfterSignup:
    def test_participants_updated_after_signup(self, client):
        # Arrange
        activity = "Science Club"
        email = "newscientist@mergington.edu"
        
        # Act - Sign up first
        client.post(f"/activities/{activity}/signup?email={email}")
        
        # Act - Get activities
        response = client.get("/activities")
        
        # Assert
        data = response.json()
        assert email in data[activity]["participants"]
