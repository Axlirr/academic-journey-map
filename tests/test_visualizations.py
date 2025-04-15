import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from ..main import app
from ..models import User, Skill, Course, Project, Goal, Achievement
from ..database import get_db

client = TestClient(app)

@pytest.fixture
def db_session(mocker):
    """Create a mock database session with test data."""
    session = mocker.Mock(spec=Session)
    
    # Create test user with sample data
    user = User(
        id=1,
        name="Test User",
        email="test@example.com"
    )
    
    # Add skills
    user.skills = [
        Skill(id=1, name="Python", category="Programming", proficiency_level=8),
        Skill(id=2, name="Data Analysis", category="Data Science", proficiency_level=7),
        Skill(id=3, name="Machine Learning", category="AI", proficiency_level=6)
    ]
    
    # Add courses
    user.courses = [
        Course(
            id=1,
            code="CS101",
            name="Intro to Programming",
            description="Basic programming concepts",
            start_date=datetime.now() - timedelta(days=180),
            skills=[user.skills[0]]
        ),
        Course(
            id=2,
            code="DS201",
            name="Data Science Fundamentals",
            description="Introduction to data science",
            start_date=datetime.now() - timedelta(days=90),
            skills=[user.skills[1], user.skills[2]]
        )
    ]
    
    # Add projects
    user.projects = [
        Project(
            id=1,
            title="ML Project",
            description="Machine learning classification project",
            skills=[user.skills[0], user.skills[2]]
        )
    ]
    
    # Add achievements
    user.achievements = [
        Achievement(
            id=1,
            title="Course Completion",
            description="Completed CS101 with distinction",
            date_achieved=datetime.now() - timedelta(days=150),
            project=user.projects[0]
        )
    ]
    
    # Add goals
    user.goals = [
        Goal(
            id=1,
            title="Master Python",
            category="Programming",
            progress=80,
            target_date=datetime.now() + timedelta(days=30)
        ),
        Goal(
            id=2,
            title="Complete ML Course",
            category="AI",
            progress=40,
            target_date=datetime.now() + timedelta(days=60)
        )
    ]
    
    session.query.return_value.filter.return_value.first.return_value = user
    return session

def test_get_skill_network(db_session, mocker):
    """Test the skill network visualization endpoint."""
    mocker.patch("app.database.get_db", return_value=db_session)
    
    response = client.get("/visualizations/skill-network/1")
    assert response.status_code == 200
    
    data = response.json()
    assert "plot_data" in data
    assert data["node_count"] > 0
    assert data["edge_count"] > 0
    assert len(data["categories"]) > 0

def test_get_skill_network_with_filters(db_session, mocker):
    """Test the skill network visualization with filters."""
    mocker.patch("app.database.get_db", return_value=db_session)
    
    response = client.get(
        "/visualizations/skill-network/1?min_proficiency=7&category_filter=Programming"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert all(skill["proficiency_level"] >= 7 for skill in data["plot_data"]["nodes"]
              if "proficiency_level" in skill)

def test_get_progress_timeline(db_session, mocker):
    """Test the progress timeline visualization endpoint."""
    mocker.patch("app.database.get_db", return_value=db_session)
    
    response = client.get("/visualizations/progress-timeline/1")
    assert response.status_code == 200
    
    data = response.json()
    assert "plot_data" in data
    assert data["event_count"] > 0
    assert "start_date" in data
    assert "end_date" in data

def test_get_skill_radar(db_session, mocker):
    """Test the skill radar visualization endpoint."""
    mocker.patch("app.database.get_db", return_value=db_session)
    
    response = client.get("/visualizations/skill-radar/1")
    assert response.status_code == 200
    
    data = response.json()
    assert "plot_data" in data
    assert data["total_skills"] > 0
    assert data["average_proficiency"] > 0
    assert len(data["skill_categories"]) > 0

def test_get_goal_progress(db_session, mocker):
    """Test the goal progress visualization endpoint."""
    mocker.patch("app.database.get_db", return_value=db_session)
    
    response = client.get("/visualizations/goal-progress/1")
    assert response.status_code == 200
    
    data = response.json()
    assert "plot_data" in data
    assert data["total_goals"] > 0
    assert 0 <= data["average_progress"] <= 100
    assert len(data["goal_categories"]) > 0

def test_user_not_found(db_session, mocker):
    """Test error handling when user is not found."""
    db_session.query.return_value.filter.return_value.first.return_value = None
    mocker.patch("app.database.get_db", return_value=db_session)
    
    endpoints = [
        "/visualizations/skill-network/999",
        "/visualizations/progress-timeline/999",
        "/visualizations/skill-radar/999",
        "/visualizations/goal-progress/999"
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

def test_invalid_parameters(db_session, mocker):
    """Test error handling with invalid parameters."""
    mocker.patch("app.database.get_db", return_value=db_session)
    
    response = client.get("/visualizations/skill-network/1?min_proficiency=11")
    assert response.status_code == 422
    
    response = client.get("/visualizations/skill-network/1?min_proficiency=0")
    assert response.status_code == 422