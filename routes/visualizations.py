from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from ..database import get_db
from ..models import User, Course, Skill, Project, Goal, Achievement
from ..visualization import AcademicVisualizer
from ..ai_service import AcademicInsightEngine

router = APIRouter(prefix="/visualizations", tags=["visualizations"])
visualizer = AcademicVisualizer()
insight_engine = AcademicInsightEngine()

@router.get("/skill-network/{user_id}")
async def get_skill_network(user_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get the interactive skill network visualization for a user."""
    # Get user data
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prepare data with AI insights
    skills = [{
        'name': skill.name,
        'proficiency_level': skill.proficiency_level,
        'category': skill.category
    } for skill in user.skills]
    
    courses = [{
        'code': course.code,
        'name': course.name,
        'description': course.description,
        'skills': [{
            'name': skill.name
        } for skill in course.skills],
        'importance_score': insight_engine.analyze_course_importance(course)
    } for course in user.courses]
    
    projects = [{
        'title': project.title,
        'description': project.description,
        'skills': [{
            'name': skill.name
        } for skill in project.skills]
    } for project in user.projects]
    
    # Generate visualization
    return visualizer.create_skill_network(skills, courses, projects)

@router.get("/progress-timeline/{user_id}")
async def get_progress_timeline(user_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get the academic progress timeline visualization for a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prepare data with AI insights
    courses = [{
        'name': course.name,
        'description': course.description,
        'year': course.year,
        'importance_score': insight_engine.analyze_course_importance(course)
    } for course in user.courses]
    
    achievements = [{
        'title': achievement.title,
        'description': achievement.description,
        'date_achieved': achievement.date_achieved,
        'impact_score': insight_engine.analyze_project_impact(achievement.project) if achievement.project else 0.5
    } for achievement in user.achievements]
    
    return visualizer.create_progress_timeline(courses, achievements)

@router.get("/skill-radar/{user_id}")
async def get_skill_radar(user_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get the skill proficiency radar chart for a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prepare data with AI insights
    skills = [{
        'name': skill.name,
        'category': skill.category,
        'proficiency_level': skill.proficiency_level,
        'market_demand': insight_engine.get_market_demand(skill.name)
    } for skill in user.skills]
    
    return visualizer.create_skill_radar(skills)

@router.get("/goal-progress/{user_id}")
async def get_goal_progress(user_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get the goal progress visualization for a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prepare data
    goals = [{
        'title': goal.title,
        'category': goal.category,
        'progress': goal.progress,
        'target_date': goal.target_date
    } for goal in user.goals]
    
    return visualizer.create_goal_progress_chart(goals)