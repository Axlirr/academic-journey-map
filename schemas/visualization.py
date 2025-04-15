from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime

class VisualizationResponse(BaseModel):
    """Base response model for all visualizations."""
    plot_data: Dict[str, Any]
    title: str
    description: str

class SkillNetworkResponse(VisualizationResponse):
    """Response model for skill network visualization."""
    node_count: int
    edge_count: int
    categories: List[str]

class TimelineResponse(VisualizationResponse):
    """Response model for progress timeline visualization."""
    start_date: datetime
    end_date: datetime
    event_count: int

class SkillRadarResponse(VisualizationResponse):
    """Response model for skill radar visualization."""
    skill_categories: List[str]
    total_skills: int
    average_proficiency: float

class GoalProgressResponse(VisualizationResponse):
    """Response model for goal progress visualization."""
    goal_categories: List[str]
    total_goals: int
    average_progress: float