import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import pandas as pd
from typing import List, Dict, Any
import json

class AcademicVisualizer:
    def __init__(self):
        self.color_palette = px.colors.qualitative.Set3
        
    def create_skill_network(self, skills: List[Dict], courses: List[Dict], projects: List[Dict]) -> Dict:
        """Create an interactive network visualization of skills, courses, and projects."""
        G = nx.Graph()
        
        # Add nodes
        for skill in skills:
            G.add_node(skill['name'], 
                      node_type='skill',
                      size=skill['proficiency_level'] * 10,
                      color=self.color_palette[0])
                      
        for course in courses:
            G.add_node(course['code'],
                      node_type='course',
                      size=30,
                      color=self.color_palette[1])
                      
        for project in projects:
            G.add_node(project['title'],
                      node_type='project',
                      size=40,
                      color=self.color_palette[2])
        
        # Add edges
        for course in courses:
            for skill in course['skills']:
                G.add_edge(course['code'], skill['name'])
                
        for project in projects:
            for skill in project['skills']:
                G.add_edge(project['title'], skill['name'])
        
        # Get node positions using force-directed layout
        pos = nx.spring_layout(G)
        
        # Create traces for nodes
        node_trace = go.Scatter(
            x=[pos[node][0] for node in G.nodes()],
            y=[pos[node][1] for node in G.nodes()],
            mode='markers+text',
            text=list(G.nodes()),
            textposition='bottom center',
            marker=dict(
                size=[G.nodes[node]['size'] for node in G.nodes()],
                color=[G.nodes[node]['color'] for node in G.nodes()],
                line=dict(width=2)
            ),
            hovertemplate='%{text}<br>Type: %{customdata[0]}<extra></extra>',
            customdata=[[G.nodes[node]['node_type']] for node in G.nodes()]
        )
        
        # Create traces for edges
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        # Create the figure
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title='Skills Network',
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           plot_bgcolor='white'
                       ))
        
        return json.loads(fig.to_json())
    
    def create_progress_timeline(self, courses: List[Dict], achievements: List[Dict]) -> Dict:
        """Create an interactive timeline of academic progress and achievements."""
        # Combine courses and achievements
        events = []
        
        for course in courses:
            events.append({
                'date': course['year'],
                'name': course['name'],
                'type': 'Course',
                'description': course['description'],
                'score': course['importance_score']
            })
            
        for achievement in achievements:
            events.append({
                'date': achievement['date_achieved'].year,
                'name': achievement['title'],
                'type': 'Achievement',
                'description': achievement['description'],
                'score': achievement['impact_score']
            })
        
        # Create DataFrame
        df = pd.DataFrame(events)
        
        # Create figure
        fig = px.timeline(df, x_start='date', y='type',
                         color='type',
                         hover_name='name',
                         hover_data=['description', 'score'],
                         title='Academic Journey Timeline')
        
        fig.update_layout(
            plot_bgcolor='white',
            showlegend=True,
            height=400
        )
        
        return json.loads(fig.to_json())
    
    def create_skill_radar(self, skills: List[Dict]) -> Dict:
        """Create a radar chart of skill proficiencies by category."""
        # Group skills by category
        skill_categories = {}
        for skill in skills:
            if skill['category'] not in skill_categories:
                skill_categories[skill['category']] = []
            skill_categories[skill['category']].append(skill)
        
        # Calculate average proficiency per category
        categories = []
        proficiencies = []
        market_demands = []
        
        for category, category_skills in skill_categories.items():
            categories.append(category)
            avg_proficiency = sum(s['proficiency_level'] for s in category_skills) / len(category_skills)
            proficiencies.append(avg_proficiency)
            avg_demand = sum(s['market_demand'] for s in category_skills) / len(category_skills)
            market_demands.append(avg_demand)
        
        # Create radar chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=proficiencies,
            theta=categories,
            fill='toself',
            name='Current Proficiency'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=market_demands,
            theta=categories,
            fill='toself',
            name='Market Demand'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )),
            showlegend=True,
            title='Skill Proficiency vs Market Demand'
        )
        
        return json.loads(fig.to_json())
    
    def create_goal_progress_chart(self, goals: List[Dict]) -> Dict:
        """Create a progress chart for academic and career goals."""
        # Prepare data
        df = pd.DataFrame(goals)
        
        # Create figure
        fig = go.Figure()
        
        for category in df['category'].unique():
            category_data = df[df['category'] == category]
            
            fig.add_trace(go.Bar(
                name=category,
                x=category_data['title'],
                y=category_data['progress'],
                text=category_data['progress'].apply(lambda x: f'{x:.0%}'),
                textposition='auto',
            ))
        
        fig.update_layout(
            title='Goal Progress by Category',
            yaxis=dict(
                title='Progress',
                tickformat='%',
                range=[0, 1]
            ),
            plot_bgcolor='white',
            barmode='group'
        )
        
        return json.loads(fig.to_json())