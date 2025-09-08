"""
📊 Progress Tracking Module
Learning analytics and progress visualization

This module implements:
- Learning progress tracking
- Performance analytics
- Weak topic identification
- Learning pattern analysis
- Progress visualization
"""

import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import streamlit as st

class ProgressTracker:
    """
    Progress tracking class for learning analytics and visualization
    Tracks user progress, identifies weak topics, and provides insights
    """
    
    def __init__(self):
        self._init_progress_data()
    
    def _init_progress_data(self):
        """Initialize progress tracking data structure"""
        if "progress_data" not in st.session_state:
            st.session_state.progress_data = {
                "user_id": "default_user",
                "total_questions": 0,
                "total_sessions": 0,
                "languages_used": {},
                "topics_covered": {},
                "learning_levels": {},
                "daily_progress": {},
                "weak_topics": {},
                "strong_topics": {},
                "learning_streak": 0,
                "last_activity": None,
                "session_history": [],
                "performance_metrics": {
                    "accuracy": 0.0,
                    "completion_rate": 0.0,
                    "engagement_score": 0.0
                }
            }
    
    def update_progress(
        self, 
        query: str, 
        response: str, 
        language: str = "en",
        learning_level: str = "beginner",
        correct: Optional[bool] = None
    ):
        """
        Update progress tracking with new interaction
        
        Args:
            query: User's question
            response: AI's response
            language: Language used
            learning_level: Learning level used
            correct: Whether the response was correct (for quizzes)
        """
        progress_data = st.session_state.progress_data
        current_date = datetime.now().date().isoformat()
        
        # Update basic metrics
        progress_data["total_questions"] += 1
        progress_data["last_activity"] = datetime.now().isoformat()
        
        # Update language usage
        progress_data["languages_used"][language] = progress_data["languages_used"].get(language, 0) + 1
        
        # Update learning level usage
        progress_data["learning_levels"][learning_level] = progress_data["learning_levels"].get(learning_level, 0) + 1
        
        # Update daily progress
        if current_date not in progress_data["daily_progress"]:
            progress_data["daily_progress"][current_date] = 0
        progress_data["daily_progress"][current_date] += 1
        
        # Extract and update topics
        topics = self._extract_topics(query + " " + response)
        for topic in topics:
            if topic not in progress_data["topics_covered"]:
                progress_data["topics_covered"][topic] = {
                    "count": 0,
                    "correct": 0,
                    "incorrect": 0,
                    "last_accessed": current_date
                }
            
            progress_data["topics_covered"][topic]["count"] += 1
            progress_data["topics_covered"][topic]["last_accessed"] = current_date
            
            if correct is not None:
                if correct:
                    progress_data["topics_covered"][topic]["correct"] += 1
                else:
                    progress_data["topics_covered"][topic]["incorrect"] += 1
        
        # Update learning streak
        self._update_learning_streak()
        
        # Update performance metrics
        self._update_performance_metrics()
        
        # Add to session history
        session_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query[:100],  # Truncate for storage
            "language": language,
            "learning_level": learning_level,
            "correct": correct,
            "topics": topics
        }
        progress_data["session_history"].append(session_entry)
        
        # Keep only last 1000 entries
        if len(progress_data["session_history"]) > 1000:
            progress_data["session_history"] = progress_data["session_history"][-1000:]
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from text (simplified implementation)"""
        # This would use more sophisticated NLP in practice
        common_topics = [
            "mathematics", "algebra", "geometry", "calculus", "statistics",
            "science", "biology", "chemistry", "physics", "earth_science",
            "history", "world_history", "african_history", "geography",
            "literature", "language_arts", "writing", "reading",
            "art", "music", "sports", "technology", "computer_science",
            "social_studies", "economics", "politics", "philosophy"
        ]
        
        topics = []
        text_lower = text.lower()
        
        for topic in common_topics:
            if topic.replace("_", " ") in text_lower or topic in text_lower:
                topics.append(topic)
        
        return topics
    
    def _update_learning_streak(self):
        """Update learning streak based on daily activity"""
        progress_data = st.session_state.progress_data
        current_date = datetime.now().date()
        
        # Check if user was active yesterday
        yesterday = (current_date - timedelta(days=1)).isoformat()
        
        if yesterday in progress_data["daily_progress"]:
            progress_data["learning_streak"] += 1
        else:
            # Check if streak should be reset
            if progress_data["learning_streak"] > 0:
                progress_data["learning_streak"] = 1  # Reset to 1 for today
    
    def _update_performance_metrics(self):
        """Update performance metrics"""
        progress_data = st.session_state.progress_data
        topics = progress_data["topics_covered"]
        
        if not topics:
            return
        
        # Calculate accuracy
        total_correct = sum(topic_data.get("correct", 0) for topic_data in topics.values())
        total_attempts = sum(topic_data.get("count", 0) for topic_data in topics.values())
        
        if total_attempts > 0:
            progress_data["performance_metrics"]["accuracy"] = total_correct / total_attempts
        
        # Calculate completion rate (simplified)
        progress_data["performance_metrics"]["completion_rate"] = min(1.0, total_attempts / 100)
        
        # Calculate engagement score
        recent_activity = len([entry for entry in progress_data["session_history"] 
                             if datetime.fromisoformat(entry["timestamp"]) > datetime.now() - timedelta(days=7)])
        progress_data["performance_metrics"]["engagement_score"] = min(1.0, recent_activity / 20)
    
    def get_progress_data(self) -> Dict:
        """Get comprehensive progress data"""
        return st.session_state.progress_data
    
    def get_learning_analytics(self) -> Dict:
        """Get detailed learning analytics"""
        progress_data = st.session_state.progress_data
        
        return {
            "overview": {
                "total_questions": progress_data["total_questions"],
                "learning_streak": progress_data["learning_streak"],
                "languages_used": len(progress_data["languages_used"]),
                "topics_covered": len(progress_data["topics_covered"]),
                "last_activity": progress_data["last_activity"]
            },
            "performance": progress_data["performance_metrics"],
            "language_distribution": progress_data["languages_used"],
            "level_distribution": progress_data["learning_levels"],
            "topic_analysis": self._analyze_topics(),
            "weak_topics": self._identify_weak_topics(),
            "strong_topics": self._identify_strong_topics(),
            "daily_activity": progress_data["daily_progress"],
            "learning_trends": self._analyze_learning_trends()
        }
    
    def _analyze_topics(self) -> Dict:
        """Analyze topic coverage and performance"""
        progress_data = st.session_state.progress_data
        topics = progress_data["topics_covered"]
        
        topic_analysis = {}
        for topic, data in topics.items():
            total = data.get("count", 0)
            correct = data.get("correct", 0)
            accuracy = correct / total if total > 0 else 0
            
            topic_analysis[topic] = {
                "total_questions": total,
                "accuracy": accuracy,
                "last_accessed": data.get("last_accessed"),
                "mastery_level": self._calculate_mastery_level(total, accuracy)
            }
        
        return topic_analysis
    
    def _calculate_mastery_level(self, total_questions: int, accuracy: float) -> str:
        """Calculate mastery level for a topic"""
        if total_questions < 3:
            return "beginner"
        elif total_questions < 8:
            if accuracy >= 0.8:
                return "intermediate"
            else:
                return "beginner"
        else:
            if accuracy >= 0.9:
                return "advanced"
            elif accuracy >= 0.7:
                return "intermediate"
            else:
                return "beginner"
    
    def _identify_weak_topics(self) -> List[Dict]:
        """Identify topics that need more practice"""
        progress_data = st.session_state.progress_data
        topics = progress_data["topics_covered"]
        
        weak_topics = []
        for topic, data in topics.items():
            total = data.get("count", 0)
            correct = data.get("correct", 0)
            accuracy = correct / total if total > 0 else 0
            
            if total >= 3 and accuracy < 0.6:
                weak_topics.append({
                    "topic": topic,
                    "accuracy": accuracy,
                    "total_questions": total,
                    "improvement_needed": True
                })
        
        return sorted(weak_topics, key=lambda x: x["accuracy"])
    
    def _identify_strong_topics(self) -> List[Dict]:
        """Identify topics where user is performing well"""
        progress_data = st.session_state.progress_data
        topics = progress_data["topics_covered"]
        
        strong_topics = []
        for topic, data in topics.items():
            total = data.get("count", 0)
            correct = data.get("correct", 0)
            accuracy = correct / total if total > 0 else 0
            
            if total >= 5 and accuracy >= 0.8:
                strong_topics.append({
                    "topic": topic,
                    "accuracy": accuracy,
                    "total_questions": total,
                    "mastery_level": "strong"
                })
        
        return sorted(strong_topics, key=lambda x: x["accuracy"], reverse=True)
    
    def _analyze_learning_trends(self) -> Dict:
        """Analyze learning trends over time"""
        progress_data = st.session_state.progress_data
        session_history = progress_data["session_history"]
        
        if not session_history:
            return {}
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(session_history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        
        # Daily activity trend
        daily_activity = df.groupby('date').size().to_dict()
        
        # Language usage trend
        language_trend = df.groupby(['date', 'language']).size().unstack(fill_value=0).to_dict()
        
        # Learning level trend
        level_trend = df.groupby(['date', 'learning_level']).size().unstack(fill_value=0).to_dict()
        
        return {
            "daily_activity": daily_activity,
            "language_trend": language_trend,
            "level_trend": level_trend
        }
    
    def create_progress_visualizations(self):
        """Create progress visualization charts"""
        analytics = self.get_learning_analytics()
        
        # Language usage pie chart
        if analytics["language_distribution"]:
            fig_lang = px.pie(
                values=list(analytics["language_distribution"].values()),
                names=list(analytics["language_distribution"].keys()),
                title="Language Usage Distribution"
            )
            st.plotly_chart(fig_lang, use_container_width=True)
        
        # Daily activity line chart
        if analytics["daily_activity"]:
            dates = list(analytics["daily_activity"].keys())
            counts = list(analytics["daily_activity"].values())
            
            fig_activity = go.Figure()
            fig_activity.add_trace(go.Scatter(
                x=dates,
                y=counts,
                mode='lines+markers',
                name='Daily Questions',
                line=dict(color='#2e8b57', width=3)
            ))
            fig_activity.update_layout(
                title="Learning Activity Over Time",
                xaxis_title="Date",
                yaxis_title="Questions Asked",
                hovermode='x unified'
            )
            st.plotly_chart(fig_activity, use_container_width=True)
        
        # Topic performance bar chart
        topic_analysis = analytics["topic_analysis"]
        if topic_analysis:
            topics = list(topic_analysis.keys())[:10]  # Top 10 topics
            accuracies = [topic_analysis[topic]["accuracy"] for topic in topics]
            
            fig_topics = px.bar(
                x=topics,
                y=accuracies,
                title="Topic Performance (Top 10)",
                labels={'x': 'Topics', 'y': 'Accuracy'},
                color=accuracies,
                color_continuous_scale='RdYlGn'
            )
            fig_topics.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_topics, use_container_width=True)
    
    def get_recommendations(self) -> List[str]:
        """Get personalized learning recommendations"""
        analytics = self.get_learning_analytics()
        recommendations = []
        
        # Weak topic recommendations
        weak_topics = analytics["weak_topics"]
        if weak_topics:
            top_weak = weak_topics[:3]
            recommendations.append(f"Focus on improving these weak topics: {', '.join([t['topic'] for t in top_weak])}")
        
        # Language recommendations
        if len(analytics["language_distribution"]) == 1:
            recommendations.append("Try practicing in different languages to improve multilingual skills")
        
        # Streak recommendations
        if analytics["overview"]["learning_streak"] < 3:
            recommendations.append("Try to maintain a daily learning streak for better progress")
        
        # Level progression recommendations
        level_dist = analytics["level_distribution"]
        if level_dist.get("beginner", 0) > 20 and level_dist.get("intermediate", 0) < 5:
            recommendations.append("Consider progressing to intermediate level for more challenging content")
        
        return recommendations
    
    def export_progress_data(self) -> str:
        """Export progress data as JSON"""
        return json.dumps(st.session_state.progress_data, indent=2, default=str)
    
    def import_progress_data(self, data: str):
        """Import progress data from JSON"""
        try:
            imported_data = json.loads(data)
            st.session_state.progress_data = imported_data
            st.success("Progress data imported successfully!")
        except Exception as e:
            st.error(f"Failed to import progress data: {e}")
    
    def reset_progress(self):
        """Reset all progress data"""
        self._init_progress_data()
        st.success("Progress data reset successfully!")
    
    def get_achievement_badges(self) -> List[Dict]:
        """Get achievement badges based on progress"""
        analytics = self.get_learning_analytics()
        badges = []
        
        # Question count badges
        total_questions = analytics["overview"]["total_questions"]
        if total_questions >= 100:
            badges.append({"name": "Century Scholar", "description": "Asked 100+ questions", "icon": "🏆"})
        elif total_questions >= 50:
            badges.append({"name": "Half Century", "description": "Asked 50+ questions", "icon": "🥈"})
        elif total_questions >= 10:
            badges.append({"name": "Getting Started", "description": "Asked 10+ questions", "icon": "🥉"})
        
        # Streak badges
        streak = analytics["overview"]["learning_streak"]
        if streak >= 30:
            badges.append({"name": "Monthly Master", "description": "30-day learning streak", "icon": "🔥"})
        elif streak >= 7:
            badges.append({"name": "Weekly Warrior", "description": "7-day learning streak", "icon": "⚡"})
        
        # Language badges
        languages_used = analytics["overview"]["languages_used"]
        if languages_used >= 4:
            badges.append({"name": "Polyglot", "description": "Used 4+ languages", "icon": "🌍"})
        elif languages_used >= 2:
            badges.append({"name": "Bilingual", "description": "Used 2+ languages", "icon": "🗣️"})
        
        return badges
