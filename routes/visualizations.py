from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from ..database import get_db
from ..models import User, Course, Skill, Project, Goal, Achievement
from ..visualization import AcademicVisualizer
from ..ai_service import AcademicInsightEngine
from ..schemas.visualization import (
    SkillNetworkResponse,
    TimelineResponse,
    SkillRadarResponse,
    GoalProgressResponse
)
from ..utils.logging import logger

router = APIRouter(prefix="/visualizations", tags=["visualizations"])
visualizer = AcademicVisualizer()
insight_engine = AcademicInsightEngine()

@router.get(
    "/skill-network/{user_id}",
    response_model=SkillNetworkResponse,
    responses={
        404: {"description": "User not found"},
        422: {"description": "Invalid parameters"},
        500: {"description": "Internal server error"}
    }
)
async def get_skill_network(
    user_id: int,
    min_proficiency: Optional[int] = Query(None, ge=1, le=10),
    category_filter: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Generate an interactive network visualization of skills, courses, and projects.

    Parameters:
    - user_id: The ID of the user
    - min_proficiency: Optional minimum proficiency level to filter skills (1-10)
    - category_filter: Optional category to filter skills by

    Returns:
    - Interactive network visualization with nodes representing skills, courses, and projects
    - Node sizes indicate proficiency levels and importance
    - Edges show relationships between nodes
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Prepare data with AI insights and filtering
        skills = [{
            'name': skill.name,
            'proficiency_level': skill.proficiency_level,
            'category': skill.category
        } for skill in user.skills
        if (min_proficiency is None or skill.proficiency_level >= min_proficiency) and
           (category_filter is None or skill.category == category_filter)]
        
        if not skills:
            raise HTTPException(
                status_code=422,
                detail="No skills found matching the specified criteria"
            )
        
        courses = [{
            'code': course.code,
            'name': course.name,
            'description': course.description,
            'skills': [{'name': skill.name} for skill in course.skills],
            'importance_score': insight_engine.analyze_course_importance(course)
        } for course in user.courses]
        
        projects = [{
            'title': project.title,
            'description': project.description,
            'skills': [{'name': skill.name} for skill in project.skills]
        } for project in user.projects]
        
        visualization = visualizer.create_skill_network(skills, courses, projects)
        
        return SkillNetworkResponse(
            plot_data=visualization,
            title=f"Skill Network for {user.name}",
            description="Interactive visualization of skills, courses, and projects",
            node_count=len(skills) + len(courses) + len(projects),
            edge_count=sum(len(c['skills']) for c in courses) + sum(len(p['skills']) for p in projects),
            categories=list(set(s['category'] for s in skills))
        )
        
    except Exception as e:
        logger.error(f"Error generating skill network: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the visualization"
        )

@router.get(
    "/progress-timeline/{user_id}",
    response_model=TimelineResponse,
    responses={
        404: {"description": "User not found"},
        422: {"description": "Invalid parameters"},
        500: {"description": "Internal server error"}
    }
)
async def get_progress_timeline(
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Generate an interactive timeline visualization of academic progress.

    Parameters:
    - user_id: The ID of the user
    - start_date: Optional start date for filtering events
    - end_date: Optional end date for filtering events

    Returns:
    - Interactive timeline showing courses and achievements
    - Color-coded events by type
    - Hover information with descriptions and impact scores
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Set default date range if not provided
        if not start_date:
            start_date = min(
                (c.start_date for c in user.courses),
                default=datetime.now() - timedelta(days=365)
            )
        if not end_date:
            end_date = max(
                (a.date_achieved for a in user.achievements),
                default=datetime.now()
            )
            
        # Prepare data with AI insights and date filtering
        courses = [{
            'name': course.name,
            'description': course.description,
            'year': course.year,
            'importance_score': insight_engine.analyze_course_importance(course)
        } for course in user.courses
        if start_date <= course.start_date <= end_date]
        
        achievements = [{
            'title': achievement.title,
            'description': achievement.description,
            'date_achieved': achievement.date_achieved,
            'impact_score': insight_engine.analyze_project_impact(achievement.project)
                if achievement.project else 0.5
        } for achievement in user.achievements
        if start_date <= achievement.date_achieved <= end_date]
        
        if not courses and not achievements:
            raise HTTPException(
                status_code=422,
                detail="No events found in the specified date range"
            )
        
        visualization = visualizer.create_progress_timeline(courses, achievements)
        
        return TimelineResponse(
            plot_data=visualization,
            title=f"Academic Progress Timeline for {user.name}",
            description="Interactive timeline of courses and achievements",
            start_date=start_date,
            end_date=end_date,
            event_count=len(courses) + len(achievements)
        )
        
    except Exception as e:
        logger.error(f"Error generating progress timeline: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the visualization"
        )

@router.get(
    "/skill-radar/{user_id}",
    response_model=SkillRadarResponse,
    responses={
        404: {"description": "User not found"},
        422: {"description": "Invalid parameters"},
        500: {"description": "Internal server error"}
    }
)
async def get_skill_radar(
    user_id: int,
    category_filter: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Generate a radar chart visualization of skill proficiencies.

    Parameters:
    - user_id: The ID of the user
    - category_filter: Optional category to filter skills by

    Returns:
    - Interactive radar chart showing skill proficiencies by category
    - Market demand comparison
    - Hover information with detailed skill data
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Prepare data with AI insights and filtering
        skills = [{
            'name': skill.name,
            'category': skill.category,
            'proficiency_level': skill.proficiency_level,
            'market_demand': insight_engine.get_market_demand(skill.name)
        } for skill in user.skills
        if category_filter is None or skill.category == category_filter]
        
        if not skills:
            raise HTTPException(
                status_code=422,
                detail="No skills found in the specified category"
            )
        
        visualization = visualizer.create_skill_radar(skills)
        
        categories = list(set(s['category'] for s in skills))
        avg_proficiency = sum(s['proficiency_level'] for s in skills) / len(skills)
        
        return SkillRadarResponse(
            plot_data=visualization,
            title=f"Skill Proficiency Radar for {user.name}",
            description="Interactive radar chart of skill proficiencies and market demand",
            skill_categories=categories,
            total_skills=len(skills),
            average_proficiency=avg_proficiency
        )
        
    except Exception as e:
        logger.error(f"Error generating skill radar: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the visualization"
        )

@router.get(
    "/goal-progress/{user_id}",
    response_model=GoalProgressResponse,
    responses={
        404: {"description": "User not found"},
        422: {"description": "Invalid parameters"},
        500: {"description": "Internal server error"}
    }
)
async def get_goal_progress(
    user_id: int,
    category_filter: Optional[str] = None,
    include_completed: bool = False,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Generate a visualization of goal progress.

    Parameters:
    - user_id: The ID of the user
    - category_filter: Optional category to filter goals by
    - include_completed: Whether to include completed goals

    Returns:
    - Interactive bar chart showing goal progress
    - Grouped by category
    - Progress percentage and target dates
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Prepare data with filtering
        goals = [{
            'title': goal.title,
            'category': goal.category,
            'progress': goal.progress,
            'target_date': goal.target_date
        } for goal in user.goals
        if (category_filter is None or goal.category == category_filter) and
           (include_completed or goal.progress < 100)]
        
        if not goals:
            raise HTTPException(
                status_code=422,
                detail="No goals found matching the specified criteria"
            )
        
        visualization = visualizer.create_goal_progress_chart(goals)
        
        categories = list(set(g['category'] for g in goals))
        avg_progress = sum(g['progress'] for g in goals) / len(goals)
        
        return GoalProgressResponse(
            plot_data=visualization,
            title=f"Goal Progress for {user.name}",
            description="Interactive visualization of goal progress by category",
            goal_categories=categories,
            total_goals=len(goals),
            average_progress=avg_progress
        )
        
    except Exception as e:
        logger.error(f"Error generating goal progress chart: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the visualization"
        )