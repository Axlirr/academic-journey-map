from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Table, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# Association tables for many-to-many relationships
skill_course = Table('skill_course', Base.metadata,
    Column('skill_id', Integer, ForeignKey('skills.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

project_skill = Table('project_skill', Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id')),
    Column('skill_id', Integer, ForeignKey('skills.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    university = Column(String)
    major = Column(String)
    graduation_year = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    courses = relationship("Course", back_populates="user")
    projects = relationship("Project", back_populates="user")
    skills = relationship("Skill", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    achievements = relationship("Achievement", back_populates="user")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    description = Column(String)
    semester = Column(String)
    year = Column(Integer)
    grade = Column(String)
    credits = Column(Float)
    status = Column(String)  # In Progress, Completed, Planned
    importance_score = Column(Float)  # AI-calculated importance for career goals
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    user = relationship("User", back_populates="courses")
    skills = relationship("Skill", secondary=skill_course, back_populates="courses")
    achievements = relationship("Achievement", back_populates="course")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)  # Technical, Soft Skills, etc.
    proficiency_level = Column(Integer)  # 1-5
    description = Column(String)
    last_used = Column(DateTime)
    growth_rate = Column(Float)  # AI-calculated skill growth rate
    market_demand = Column(Float)  # AI-calculated market demand
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    user = relationship("User", back_populates="skills")
    courses = relationship("Course", secondary=skill_course, back_populates="skills")
    projects = relationship("Project", secondary=project_skill, back_populates="skills")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String)  # In Progress, Completed, Planned
    github_url = Column(String)
    demo_url = Column(String)
    impact_score = Column(Float)  # AI-calculated project impact
    complexity_score = Column(Float)  # AI-calculated complexity
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    user = relationship("User", back_populates="projects")
    skills = relationship("Skill", secondary=project_skill, back_populates="projects")
    achievements = relationship("Achievement", back_populates="project")

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    category = Column(String)  # Academic, Career, Skill Development
    target_date = Column(DateTime)
    status = Column(String)  # Not Started, In Progress, Achieved
    progress = Column(Float)
    priority = Column(Integer)
    ai_recommendations = Column(JSON)  # AI-generated recommendations
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    user = relationship("User", back_populates="goals")

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    date_achieved = Column(DateTime)
    category = Column(String)  # Academic, Project, Extra-curricular
    impact_score = Column(Float)  # AI-calculated achievement impact
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    course = relationship("Course", back_populates="achievements")
    project = relationship("Project", back_populates="achievements")