from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import FileResponse
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
from ..utils.cache import cache_visualization, invalidate_user_cache, get_cache_stats
from ..utils.export import VisualizationExporter

router = APIRouter(prefix="/visualizations", tags=["visualizations"])
visualizer = AcademicVisualizer()
insight_engine = AcademicInsightEngine()
exporter = VisualizationExporter()

@router.get(
    "/skill-network/{user_id}",
    response_model=SkillNetworkResponse,
    responses={
        404: {"description": "User not found"},
        422: {"description": "Invalid parameters"},
        500: {"description": "Internal server error"}
    }
)
@cache_visualization(prefix="viz:skill")
async def get_skill_network(
    user_id: int,
    min_proficiency: Optional[int] = Query(None, ge=1, le=10),
    category_filter: Optional[str] = None,
    response: Response = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Generate an interactive network visualization of skills, courses, and projects."""
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
        
        # Set cache control headers
        if response:
            response.headers["Cache-Control"] = "max-age=3600"
            response.headers["ETag"] = f"skill-network-{user_id}-{len(skills)}"
        
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
    "/skill-network/{user_id}/export",
    responses={
        200: {"description": "Successful export"},
        404: {"description": "User not found"},
        422: {"description": "Invalid parameters"}
    }
)
async def export_skill_network(
    user_id: int,
    format: str = Query(..., regex="^(html|png|svg|pdf|json|csv)$"),
    filename: Optional[str] = None,
    db: Session = Depends(get_db)
) -> FileResponse:
    """Export the skill network visualization in the specified format."""
    try:
        visualization_data = await get_skill_network(user_id, db=db)
        
        filepath = exporter.export(
            visualization_data.dict(),
            format=format,
            filename=filename
        )
        
        return FileResponse(
            filepath,
            filename=f"skill_network_{user_id}.{format}",
            media_type=f"application/{format}"
        )
        
    except Exception as e:
        logger.error(f"Export error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred during export"
        )

# Similar updates for other visualization endpoints...

@router.post("/cache/invalidate/{user_id}")
async def invalidate_visualizations_cache(
    user_id: int,
    visualization_type: Optional[str] = None
) -> Dict[str, str]:
    """Invalidate cached visualizations for a user."""
    try:
        invalidate_user_cache(user_id, prefix=visualization_type)
        return {"message": "Cache invalidated successfully"}
    except Exception as e:
        logger.error(f"Cache invalidation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to invalidate cache"
        )

@router.get("/cache/stats")
async def get_visualization_cache_stats() -> Dict[str, int]:
    """Get statistics about cached visualizations."""
    return get_cache_stats()

@router.get("/export/formats")
async def get_supported_export_formats() -> Dict[str, str]:
    """Get list of supported export formats."""
    return VisualizationExporter.SUPPORTED_FORMATS