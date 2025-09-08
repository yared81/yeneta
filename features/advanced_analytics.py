"""
Advanced Analytics & Learning Insights

This module provides comprehensive analytics and insights for student learning
patterns, performance prediction, and personalized recommendations.
"""

import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging
import pandas as pd

logger = logging.getLogger(__name__)

class AdvancedAnalytics:
    """
    Advanced analytics engine for learning insights, performance prediction,
    and personalized recommendations.
    """
    
    def __init__(self):
        self.learning_patterns = {}
        self.performance_history = {}
        self.engagement_metrics = {}
        
    def analyze_learning_style(self, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze student's learning style based on interaction patterns.
        
        Args:
            interaction_data: Dictionary containing interaction data
            
        Returns:
            Dictionary with learning style analysis
        """
        try:
            # Extract features
            video_watch_time = interaction_data.get("video_watch_time", 0)
            text_read_time = interaction_data.get("text_read_time", 0)
            audio_listen_time = interaction_data.get("audio_listen_time", 0)
            hands_on_activities = interaction_data.get("hands_on_activities", 0)
            total_time = video_watch_time + text_read_time + audio_listen_time + hands_on_activities
            
            if total_time == 0:
                return {"learning_style": "mixed", "confidence": 0.5}
            
            # Calculate percentages
            video_pct = video_watch_time / total_time
            text_pct = text_read_time / total_time
            audio_pct = audio_listen_time / total_time
            hands_on_pct = hands_on_activities / total_time
            
            # Determine dominant learning style
            styles = {
                "visual": video_pct,
                "reading": text_pct,
                "auditory": audio_pct,
                "kinesthetic": hands_on_pct
            }
            
            dominant_style = max(styles, key=styles.get)
            confidence = max(styles.values())
            
            return {
                "learning_style": dominant_style,
                "confidence": confidence,
                "style_breakdown": styles,
                "recommendations": self._get_style_recommendations(dominant_style)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing learning style: {e}")
            return {"learning_style": "mixed", "confidence": 0.5}
    
    def predict_performance(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict student performance based on historical data.
        
        Args:
            student_data: Dictionary containing student performance data
            
        Returns:
            Dictionary with performance predictions
        """
        try:
            # Extract features
            avg_score = student_data.get("average_score", 0)
            completion_rate = student_data.get("completion_rate", 0)
            study_consistency = student_data.get("study_consistency", 0)
            time_per_module = student_data.get("average_time_per_module", 0)
            engagement_score = student_data.get("engagement_score", 0)
            
            # Simple prediction model (in production, use ML models)
            performance_score = (
                avg_score * 0.3 +
                completion_rate * 100 * 0.25 +
                study_consistency * 100 * 0.2 +
                min(100, max(0, 100 - time_per_module)) * 0.15 +
                engagement_score * 0.1
            )
            
            # Predict exam performance
            exam_prediction = min(100, max(0, performance_score + np.random.normal(0, 5)))
            
            # Predict time to mastery
            time_to_mastery = self._calculate_time_to_mastery(student_data)
            
            # Risk assessment
            risk_factors = self._assess_risk_factors(student_data)
            
            return {
                "predicted_exam_score": round(exam_prediction, 1),
                "confidence_level": self._calculate_confidence(student_data),
                "time_to_mastery_weeks": time_to_mastery,
                "performance_trend": self._analyze_performance_trend(student_data),
                "risk_factors": risk_factors,
                "recommendations": self._generate_performance_recommendations(student_data)
            }
            
        except Exception as e:
            logger.error(f"Error predicting performance: {e}")
            return {"predicted_exam_score": 0, "confidence_level": 0}
    
    def analyze_weakness_patterns(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze patterns in student weaknesses and struggles.
        
        Args:
            performance_data: Dictionary containing performance data
            
        Returns:
            Dictionary with weakness analysis
        """
        try:
            weak_areas = performance_data.get("weak_areas", [])
            error_patterns = performance_data.get("error_patterns", [])
            time_spent = performance_data.get("time_spent_by_topic", {})
            
            # Analyze common error types
            error_analysis = self._analyze_error_patterns(error_patterns)
            
            # Identify struggling topics
            struggling_topics = self._identify_struggling_topics(weak_areas, time_spent)
            
            # Generate intervention strategies
            interventions = self._generate_interventions(struggling_topics, error_analysis)
            
            return {
                "struggling_topics": struggling_topics,
                "error_patterns": error_analysis,
                "intervention_strategies": interventions,
                "priority_areas": self._prioritize_areas(struggling_topics),
                "estimated_improvement_time": self._estimate_improvement_time(struggling_topics)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing weakness patterns: {e}")
            return {"struggling_topics": [], "error_patterns": {}}
    
    def generate_learning_insights(self, student_id: str, time_period: str = "30d") -> Dict[str, Any]:
        """
        Generate comprehensive learning insights for a student.
        
        Args:
            student_id: Unique student identifier
            time_period: Time period for analysis (7d, 30d, 90d)
            
        Returns:
            Dictionary with comprehensive learning insights
        """
        try:
            # Get student data
            student_data = self._get_student_data(student_id, time_period)
            
            # Learning style analysis
            learning_style = self.analyze_learning_style(student_data.get("interaction_data", {}))
            
            # Performance prediction
            performance_prediction = self.predict_performance(student_data)
            
            # Weakness analysis
            weakness_analysis = self.analyze_weakness_patterns(student_data)
            
            # Engagement analysis
            engagement_analysis = self._analyze_engagement(student_data)
            
            # Learning efficiency
            efficiency_analysis = self._analyze_learning_efficiency(student_data)
            
            # Generate recommendations
            recommendations = self._generate_comprehensive_recommendations(
                learning_style, performance_prediction, weakness_analysis, 
                engagement_analysis, efficiency_analysis
            )
            
            return {
                "student_id": student_id,
                "analysis_period": time_period,
                "generated_at": datetime.now().isoformat(),
                "learning_style": learning_style,
                "performance_prediction": performance_prediction,
                "weakness_analysis": weakness_analysis,
                "engagement_analysis": engagement_analysis,
                "efficiency_analysis": efficiency_analysis,
                "recommendations": recommendations,
                "overall_insights": self._generate_overall_insights(
                    learning_style, performance_prediction, weakness_analysis
                )
            }
            
        except Exception as e:
            logger.error(f"Error generating learning insights: {e}")
            return {"error": str(e)}
    
    def _get_style_recommendations(self, learning_style: str) -> List[str]:
        """Get recommendations based on learning style."""
        recommendations = {
            "visual": [
                "Use diagrams and charts to understand concepts",
                "Watch educational videos and animations",
                "Create mind maps and visual notes",
                "Use color coding in your study materials"
            ],
            "auditory": [
                "Listen to audio lectures and podcasts",
                "Participate in group discussions",
                "Record yourself explaining concepts",
                "Use mnemonic devices and rhymes"
            ],
            "reading": [
                "Read textbooks and written materials",
                "Take detailed written notes",
                "Write summaries and explanations",
                "Use flashcards for memorization"
            ],
            "kinesthetic": [
                "Engage in hands-on activities and experiments",
                "Use physical models and simulations",
                "Take frequent breaks to move around",
                "Practice with real-world applications"
            ]
        }
        return recommendations.get(learning_style, recommendations["mixed"])
    
    def _calculate_time_to_mastery(self, student_data: Dict[str, Any]) -> int:
        """Calculate estimated time to mastery in weeks."""
        current_level = student_data.get("current_level", "beginner")
        target_level = student_data.get("target_level", "advanced")
        study_hours_per_week = student_data.get("study_hours_per_week", 5)
        
        level_hours = {
            "beginner": 0,
            "intermediate": 40,
            "advanced": 80
        }
        
        current_hours = level_hours.get(current_level, 0)
        target_hours = level_hours.get(target_level, 80)
        
        remaining_hours = target_hours - current_hours
        return max(1, remaining_hours // study_hours_per_week)
    
    def _assess_risk_factors(self, student_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Assess risk factors for student success."""
        risk_factors = []
        
        if student_data.get("completion_rate", 0) < 0.7:
            risk_factors.append({
                "factor": "Low completion rate",
                "severity": "high",
                "description": "Student is not completing assigned work consistently"
            })
        
        if student_data.get("average_score", 0) < 60:
            risk_factors.append({
                "factor": "Low performance scores",
                "severity": "high",
                "description": "Student is struggling with content comprehension"
            })
        
        if student_data.get("study_consistency", 0) < 0.5:
            risk_factors.append({
                "factor": "Inconsistent study habits",
                "severity": "medium",
                "description": "Student has irregular study patterns"
            })
        
        if student_data.get("engagement_score", 0) < 0.6:
            risk_factors.append({
                "factor": "Low engagement",
                "severity": "medium",
                "description": "Student shows low interest in learning activities"
            })
        
        return risk_factors
    
    def _calculate_confidence(self, student_data: Dict[str, Any]) -> float:
        """Calculate confidence level for predictions."""
        data_points = len([v for v in student_data.values() if v is not None])
        consistency = student_data.get("study_consistency", 0.5)
        
        # More data points and higher consistency = higher confidence
        confidence = min(0.95, (data_points / 10) * 0.5 + consistency * 0.5)
        return round(confidence, 2)
    
    def _analyze_performance_trend(self, student_data: Dict[str, Any]) -> str:
        """Analyze performance trend over time."""
        recent_scores = student_data.get("recent_scores", [])
        if len(recent_scores) < 2:
            return "insufficient_data"
        
        # Simple trend analysis
        if recent_scores[-1] > recent_scores[0]:
            return "improving"
        elif recent_scores[-1] < recent_scores[0]:
            return "declining"
        else:
            return "stable"
    
    def _generate_performance_recommendations(self, student_data: Dict[str, Any]) -> List[str]:
        """Generate performance-based recommendations."""
        recommendations = []
        
        if student_data.get("average_score", 0) < 70:
            recommendations.append("Focus on foundational concepts before advancing")
        
        if student_data.get("completion_rate", 0) < 0.8:
            recommendations.append("Set up a consistent study schedule")
        
        if student_data.get("time_per_module", 0) > 15:
            recommendations.append("Break down complex topics into smaller chunks")
        
        if student_data.get("engagement_score", 0) < 0.6:
            recommendations.append("Try different learning methods to increase engagement")
        
        return recommendations
    
    def _analyze_error_patterns(self, error_patterns: List[str]) -> Dict[str, int]:
        """Analyze common error patterns."""
        error_counts = {}
        for error in error_patterns:
            error_counts[error] = error_counts.get(error, 0) + 1
        return error_counts
    
    def _identify_struggling_topics(self, weak_areas: List[str], time_spent: Dict[str, int]) -> List[Dict[str, Any]]:
        """Identify topics where student is struggling."""
        struggling_topics = []
        
        for area in weak_areas:
            time_invested = time_spent.get(area, 0)
            struggling_topics.append({
                "topic": area,
                "time_invested": time_invested,
                "difficulty_level": "high" if time_invested > 20 else "medium",
                "priority": "high" if time_invested > 30 else "medium"
            })
        
        return sorted(struggling_topics, key=lambda x: x["time_invested"], reverse=True)
    
    def _generate_interventions(self, struggling_topics: List[Dict[str, Any]], error_analysis: Dict[str, int]) -> List[Dict[str, str]]:
        """Generate intervention strategies."""
        interventions = []
        
        for topic in struggling_topics:
            interventions.append({
                "topic": topic["topic"],
                "strategy": f"Provide additional practice exercises for {topic['topic']}",
                "type": "practice"
            })
        
        for error_type, count in error_analysis.items():
            if count > 3:  # Common error
                interventions.append({
                    "topic": error_type,
                    "strategy": f"Address common {error_type} errors with targeted instruction",
                    "type": "instruction"
                })
        
        return interventions
    
    def _prioritize_areas(self, struggling_topics: List[Dict[str, Any]]) -> List[str]:
        """Prioritize areas for improvement."""
        return [topic["topic"] for topic in struggling_topics if topic["priority"] == "high"]
    
    def _estimate_improvement_time(self, struggling_topics: List[Dict[str, Any]]) -> int:
        """Estimate time needed for improvement in weeks."""
        total_time = sum(topic["time_invested"] for topic in struggling_topics)
        return max(1, total_time // 10)  # Rough estimate
    
    def _get_student_data(self, student_id: str, time_period: str) -> Dict[str, Any]:
        """Get student data for analysis (mock implementation)."""
        # In production, this would fetch from database
        return {
            "interaction_data": {
                "video_watch_time": 120,
                "text_read_time": 180,
                "audio_listen_time": 60,
                "hands_on_activities": 90
            },
            "average_score": 75,
            "completion_rate": 0.8,
            "study_consistency": 0.7,
            "average_time_per_module": 12,
            "engagement_score": 0.75,
            "recent_scores": [70, 75, 80, 78],
            "weak_areas": ["algebra", "geometry"],
            "error_patterns": ["calculation_error", "concept_misunderstanding"],
            "time_spent_by_topic": {"algebra": 25, "geometry": 20, "arithmetic": 15}
        }
    
    def _analyze_engagement(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze student engagement patterns."""
        engagement_score = student_data.get("engagement_score", 0)
        
        return {
            "overall_engagement": engagement_score,
            "engagement_level": "high" if engagement_score > 0.8 else "medium" if engagement_score > 0.6 else "low",
            "engagement_trend": "stable",  # Would be calculated from historical data
            "recommendations": self._get_engagement_recommendations(engagement_score)
        }
    
    def _analyze_learning_efficiency(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze learning efficiency metrics."""
        time_per_module = student_data.get("average_time_per_module", 0)
        completion_rate = student_data.get("completion_rate", 0)
        
        efficiency_score = min(100, max(0, (completion_rate * 100) - (time_per_module * 2)))
        
        return {
            "efficiency_score": efficiency_score,
            "time_per_module": time_per_module,
            "completion_rate": completion_rate,
            "efficiency_level": "high" if efficiency_score > 80 else "medium" if efficiency_score > 60 else "low",
            "recommendations": self._get_efficiency_recommendations(efficiency_score, time_per_module)
        }
    
    def _get_engagement_recommendations(self, engagement_score: float) -> List[str]:
        """Get engagement improvement recommendations."""
        if engagement_score < 0.6:
            return [
                "Try interactive learning activities",
                "Set up study groups with peers",
                "Use gamification elements",
                "Take breaks between study sessions"
            ]
        return ["Continue current engagement strategies"]
    
    def _get_efficiency_recommendations(self, efficiency_score: float, time_per_module: int) -> List[str]:
        """Get efficiency improvement recommendations."""
        recommendations = []
        
        if efficiency_score < 60:
            recommendations.append("Focus on active learning techniques")
        
        if time_per_module > 15:
            recommendations.append("Break down complex topics into smaller chunks")
        
        if efficiency_score > 80:
            recommendations.append("Consider advancing to more challenging material")
        
        return recommendations
    
    def _generate_comprehensive_recommendations(self, learning_style, performance_prediction, 
                                              weakness_analysis, engagement_analysis, efficiency_analysis) -> List[Dict[str, str]]:
        """Generate comprehensive recommendations."""
        recommendations = []
        
        # Learning style recommendations
        for rec in learning_style.get("recommendations", []):
            recommendations.append({"type": "learning_style", "recommendation": rec})
        
        # Performance recommendations
        for rec in performance_prediction.get("recommendations", []):
            recommendations.append({"type": "performance", "recommendation": rec})
        
        # Engagement recommendations
        for rec in engagement_analysis.get("recommendations", []):
            recommendations.append({"type": "engagement", "recommendation": rec})
        
        # Efficiency recommendations
        for rec in efficiency_analysis.get("recommendations", []):
            recommendations.append({"type": "efficiency", "recommendation": rec})
        
        return recommendations
    
    def _generate_overall_insights(self, learning_style, performance_prediction, weakness_analysis) -> List[str]:
        """Generate overall insights summary."""
        insights = []
        
        if learning_style.get("confidence", 0) > 0.8:
            insights.append(f"Strong {learning_style['learning_style']} learning preference identified")
        
        if performance_prediction.get("predicted_exam_score", 0) > 80:
            insights.append("Excellent performance trajectory predicted")
        elif performance_prediction.get("predicted_exam_score", 0) < 60:
            insights.append("Performance improvement needed - consider additional support")
        
        if len(weakness_analysis.get("struggling_topics", [])) > 0:
            insights.append(f"Focus areas identified: {', '.join(weakness_analysis['struggling_topics'][:3])}")
        
        return insights
