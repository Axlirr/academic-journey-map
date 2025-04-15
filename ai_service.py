import openai
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from typing import List, Dict, Any

# Download required NLTK data
nltk.download('stopwords')
nltk.download('punkt')

class AcademicInsightEngine:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.openai_api_key
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    async def analyze_course_importance(self, course_data: Dict, career_goals: List[str]) -> float:
        """Calculate course importance based on career goals and market trends."""
        try:
            prompt = f"""
            Analyze the importance of this course for the given career goals:
            Course: {course_data['name']} - {course_data['description']}
            Career Goals: {', '.join(career_goals)}
            
            Rate the importance from 0 to 1 and explain why.
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=150
            )
            
            # Extract numerical score from response
            response_text = response.choices[0].message.content
            importance_score = float([x for x in response_text.split() if x.replace('.', '').isdigit()][0])
            return min(max(importance_score, 0), 1)  # Ensure score is between 0 and 1
            
        except Exception as e:
            print(f"Error in analyze_course_importance: {str(e)}")
            return 0.5  # Default middle score
    
    async def calculate_skill_growth(self, skill_data: Dict, user_activities: List[Dict]) -> float:
        """Calculate skill growth rate based on user activities and progress."""
        try:
            # Extract relevant activities
            relevant_activities = [
                activity for activity in user_activities
                if skill_data['name'].lower() in activity['description'].lower()
            ]
            
            # Calculate growth based on activity frequency and complexity
            if not relevant_activities:
                return 0.0
                
            activity_dates = [datetime.strptime(act['date'], '%Y-%m-%d') for act in relevant_activities]
            frequency = len(activity_dates) / max((datetime.now() - min(activity_dates)).days, 1)
            
            # Calculate complexity trend
            complexity_scores = [act.get('complexity', 0.5) for act in relevant_activities]
            growth_trend = np.polyfit(range(len(complexity_scores)), complexity_scores, 1)[0]
            
            return min(max(frequency * growth_trend * 10, 0), 1)  # Normalize between 0 and 1
            
        except Exception as e:
            print(f"Error in calculate_skill_growth: {str(e)}")
            return 0.0
    
    async def get_market_demand(self, skill_name: str) -> float:
        """Analyze market demand for a skill using job posting data."""
        try:
            # Simulate job market API call (replace with actual API in production)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Search major job sites for the skill
            job_sites = [
                f"https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id=YOUR_APP_ID&app_key=YOUR_APP_KEY&what={skill_name}",
                # Add more job sites/APIs here
            ]
            
            total_postings = 0
            for site in job_sites:
                response = requests.get(site, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    total_postings += data.get('count', 0)
            
            # Normalize the demand score
            demand_score = min(total_postings / 1000, 1)  # Normalize to 0-1
            return demand_score
            
        except Exception as e:
            print(f"Error in get_market_demand: {str(e)}")
            return 0.5  # Default middle score
    
    async def generate_career_recommendations(self, user_data: Dict) -> List[Dict]:
        """Generate personalized career recommendations based on user's profile."""
        try:
            # Prepare user profile summary
            profile_summary = f"""
            Major: {user_data['major']}
            Skills: {', '.join(user_data['skills'])}
            Courses: {', '.join(user_data['courses'])}
            Projects: {', '.join(user_data['projects'])}
            Goals: {', '.join(user_data['goals'])}
            """
            
            prompt = f"""
            Based on this student's profile, suggest 3 career paths with explanations:
            {profile_summary}
            
            For each career path, include:
            1. Job title
            2. Required skills they already have
            3. Skills they need to develop
            4. Recommended next steps
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=500
            )
            
            # Parse and structure the recommendations
            recommendations = self._parse_career_recommendations(response.choices[0].message.content)
            return recommendations
            
        except Exception as e:
            print(f"Error in generate_career_recommendations: {str(e)}")
            return []
    
    def _parse_career_recommendations(self, response_text: str) -> List[Dict]:
        """Parse the GPT response into structured career recommendations."""
        recommendations = []
        current_rec = {}
        
        for line in response_text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('1.') or line.startswith('2.') or line.startswith('3.'):
                if current_rec:
                    recommendations.append(current_rec)
                current_rec = {'title': line.split('.')[1].strip()}
            elif 'Required skills' in line:
                current_rec['existing_skills'] = [s.strip() for s in line.split(':')[1].split(',')]
            elif 'Skills they need' in line:
                current_rec['skills_to_develop'] = [s.strip() for s in line.split(':')[1].split(',')]
            elif 'Recommended next steps' in line:
                current_rec['next_steps'] = [s.strip() for s in line.split(':')[1].split(',')]
        
        if current_rec:
            recommendations.append(current_rec)
            
        return recommendations
    
    async def analyze_project_impact(self, project_data: Dict) -> float:
        """Calculate project impact score based on complexity and relevance."""
        try:
            prompt = f"""
            Analyze this project's impact and complexity:
            Title: {project_data['title']}
            Description: {project_data['description']}
            Technologies: {', '.join(project_data.get('technologies', []))}
            
            Rate the impact from 0 to 1 and explain why.
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=150
            )
            
            # Extract numerical score from response
            response_text = response.choices[0].message.content
            impact_score = float([x for x in response_text.split() if x.replace('.', '').isdigit()][0])
            return min(max(impact_score, 0), 1)  # Ensure score is between 0 and 1
            
        except Exception as e:
            print(f"Error in analyze_project_impact: {str(e)}")
            return 0.5  # Default middle score