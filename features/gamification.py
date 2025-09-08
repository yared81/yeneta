"""
Gamification & Engagement Features

This module implements gamification elements to increase student engagement
and motivation through achievements, badges, streaks, and interactive elements.
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class GamificationEngine:
    """
    Gamification engine that provides achievements, badges, streaks,
    and other engagement features to motivate students.
    """
    
    def __init__(self):
        self.achievements = self._initialize_achievements()
        self.badges = self._initialize_badges()
        self.streak_tracker = {}
        self.point_system = {}
        
    def _initialize_achievements(self) -> Dict[str, Dict[str, Any]]:
        """Initialize available achievements."""
        return {
            "first_question": {
                "id": "first_question",
                "name": "First Steps",
                "description": "Ask your first question",
                "icon": "🌱",
                "points": 10,
                "category": "milestone",
                "requirements": {"questions_asked": 1}
            },
            "language_explorer": {
                "id": "language_explorer",
                "name": "Language Explorer",
                "description": "Use 3 different languages",
                "icon": "🌍",
                "points": 25,
                "category": "exploration",
                "requirements": {"languages_used": 3}
            },
            "streak_master": {
                "id": "streak_master",
                "name": "Streak Master",
                "description": "Study for 7 consecutive days",
                "icon": "🔥",
                "points": 50,
                "category": "consistency",
                "requirements": {"study_streak": 7}
            },
            "knowledge_seeker": {
                "id": "knowledge_seeker",
                "name": "Knowledge Seeker",
                "description": "Ask 100 questions",
                "icon": "🔍",
                "points": 100,
                "category": "milestone",
                "requirements": {"questions_asked": 100}
            },
            "multilingual_master": {
                "id": "multilingual_master",
                "name": "Multilingual Master",
                "description": "Use all 6 supported languages",
                "icon": "🗣️",
                "points": 75,
                "category": "achievement",
                "requirements": {"languages_used": 6}
            },
            "speed_learner": {
                "id": "speed_learner",
                "name": "Speed Learner",
                "description": "Complete 5 modules in one day",
                "icon": "⚡",
                "points": 40,
                "category": "efficiency",
                "requirements": {"modules_completed_daily": 5}
            },
            "helpful_peer": {
                "id": "helpful_peer",
                "name": "Helpful Peer",
                "description": "Help 10 other students",
                "icon": "🤝",
                "points": 60,
                "category": "social",
                "requirements": {"students_helped": 10}
            },
            "perfect_score": {
                "id": "perfect_score",
                "name": "Perfect Score",
                "description": "Get 100% on 5 assessments",
                "icon": "💯",
                "points": 80,
                "category": "excellence",
                "requirements": {"perfect_scores": 5}
            },
            "early_bird": {
                "id": "early_bird",
                "name": "Early Bird",
                "description": "Study before 8 AM for 5 days",
                "icon": "🐦",
                "points": 30,
                "category": "habit",
                "requirements": {"early_study_days": 5}
            },
            "night_owl": {
                "id": "night_owl",
                "name": "Night Owl",
                "description": "Study after 10 PM for 5 days",
                "icon": "🦉",
                "points": 30,
                "category": "habit",
                "requirements": {"late_study_days": 5}
            }
        }
    
    def _initialize_badges(self) -> Dict[str, Dict[str, Any]]:
        """Initialize available badges."""
        return {
            "bronze_learner": {
                "id": "bronze_learner",
                "name": "Bronze Learner",
                "description": "Earned 100 points",
                "icon": "🥉",
                "points_required": 100,
                "rarity": "common"
            },
            "silver_learner": {
                "id": "silver_learner",
                "name": "Silver Learner",
                "description": "Earned 500 points",
                "icon": "🥈",
                "points_required": 500,
                "rarity": "uncommon"
            },
            "gold_learner": {
                "id": "gold_learner",
                "name": "Gold Learner",
                "description": "Earned 1000 points",
                "icon": "🥇",
                "points_required": 1000,
                "rarity": "rare"
            },
            "platinum_learner": {
                "id": "platinum_learner",
                "name": "Platinum Learner",
                "description": "Earned 2500 points",
                "icon": "💎",
                "points_required": 2500,
                "rarity": "epic"
            },
            "diamond_learner": {
                "id": "diamond_learner",
                "name": "Diamond Learner",
                "description": "Earned 5000 points",
                "icon": "💠",
                "points_required": 5000,
                "rarity": "legendary"
            }
        }
    
    def check_achievements(self, student_id: str, activity_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Check if student has earned any new achievements.
        
        Args:
            student_id: Unique student identifier
            activity_data: Current activity data
            
        Returns:
            List of newly earned achievements
        """
        try:
            # Get student's current progress
            student_progress = self._get_student_progress(student_id)
            
            new_achievements = []
            
            for achievement_id, achievement in self.achievements.items():
                # Skip if already earned
                if achievement_id in student_progress.get("earned_achievements", []):
                    continue
                
                # Check if requirements are met
                if self._check_achievement_requirements(achievement, activity_data, student_progress):
                    new_achievements.append({
                        "achievement": achievement,
                        "earned_at": datetime.now().isoformat(),
                        "points_awarded": achievement["points"]
                    })
                    
                    # Update student progress
                    self._update_student_progress(student_id, achievement_id, achievement["points"])
            
            return new_achievements
            
        except Exception as e:
            logger.error(f"Error checking achievements: {e}")
            return []
    
    def check_badges(self, student_id: str) -> List[Dict[str, Any]]:
        """
        Check if student has earned any new badges.
        
        Args:
            student_id: Unique student identifier
            
        Returns:
            List of newly earned badges
        """
        try:
            student_progress = self._get_student_progress(student_id)
            total_points = student_progress.get("total_points", 0)
            earned_badges = student_progress.get("earned_badges", [])
            
            new_badges = []
            
            for badge_id, badge in self.badges.items():
                # Skip if already earned
                if badge_id in earned_badges:
                    continue
                
                # Check if points requirement is met
                if total_points >= badge["points_required"]:
                    new_badges.append({
                        "badge": badge,
                        "earned_at": datetime.now().isoformat()
                    })
                    
                    # Update student progress
                    self._update_student_badges(student_id, badge_id)
            
            return new_badges
            
        except Exception as e:
            logger.error(f"Error checking badges: {e}")
            return []
    
    def update_study_streak(self, student_id: str, study_date: datetime = None) -> Dict[str, Any]:
        """
        Update and track study streak for a student.
        
        Args:
            student_id: Unique student identifier
            study_date: Date of study activity (defaults to now)
            
        Returns:
            Dictionary with streak information
        """
        try:
            if study_date is None:
                study_date = datetime.now()
            
            # Get current streak data
            streak_data = self.streak_tracker.get(student_id, {
                "current_streak": 0,
                "longest_streak": 0,
                "last_study_date": None
            })
            
            last_study = streak_data.get("last_study_date")
            current_streak = streak_data.get("current_streak", 0)
            
            # Check if this is a new day
            if last_study is None or study_date.date() > last_study.date():
                # Check if it's consecutive (within 2 days)
                if last_study is None or (study_date.date() - last_study.date()).days <= 1:
                    current_streak += 1
                else:
                    current_streak = 1  # Reset streak
                
                # Update longest streak
                longest_streak = max(current_streak, streak_data.get("longest_streak", 0))
                
                # Update streak data
                self.streak_tracker[student_id] = {
                    "current_streak": current_streak,
                    "longest_streak": longest_streak,
                    "last_study_date": study_date
                }
                
                # Check for streak achievements
                streak_achievements = self._check_streak_achievements(student_id, current_streak)
                
                return {
                    "current_streak": current_streak,
                    "longest_streak": longest_streak,
                    "streak_achievements": streak_achievements,
                    "next_milestone": self._get_next_streak_milestone(current_streak)
                }
            
            return {
                "current_streak": current_streak,
                "longest_streak": streak_data.get("longest_streak", 0),
                "streak_achievements": [],
                "next_milestone": self._get_next_streak_milestone(current_streak)
            }
            
        except Exception as e:
            logger.error(f"Error updating study streak: {e}")
            return {"current_streak": 0, "longest_streak": 0}
    
    def generate_leaderboard(self, time_period: str = "weekly") -> List[Dict[str, Any]]:
        """
        Generate leaderboard for students.
        
        Args:
            time_period: Time period for leaderboard (daily, weekly, monthly, all_time)
            
        Returns:
            List of students ranked by points
        """
        try:
            # Get all students and their points
            all_students = self._get_all_students_data()
            
            # Filter by time period
            filtered_students = self._filter_by_time_period(all_students, time_period)
            
            # Sort by points
            leaderboard = sorted(filtered_students, key=lambda x: x.get("points", 0), reverse=True)
            
            # Add ranking
            for i, student in enumerate(leaderboard):
                student["rank"] = i + 1
                student["tier"] = self._get_student_tier(student.get("points", 0))
            
            return leaderboard[:50]  # Top 50
            
        except Exception as e:
            logger.error(f"Error generating leaderboard: {e}")
            return []
    
    def create_learning_challenge(self, challenge_type: str, duration_days: int, 
                                requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a learning challenge for students.
        
        Args:
            challenge_type: Type of challenge
            duration_days: Duration in days
            requirements: Challenge requirements
            
        Returns:
            Dictionary with challenge details
        """
        try:
            challenge_id = f"challenge_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            challenge = {
                "id": challenge_id,
                "type": challenge_type,
                "name": self._get_challenge_name(challenge_type),
                "description": self._get_challenge_description(challenge_type),
                "duration_days": duration_days,
                "requirements": requirements,
                "rewards": self._get_challenge_rewards(challenge_type),
                "start_date": datetime.now().isoformat(),
                "end_date": (datetime.now() + timedelta(days=duration_days)).isoformat(),
                "participants": [],
                "status": "active"
            }
            
            return challenge
            
        except Exception as e:
            logger.error(f"Error creating learning challenge: {e}")
            return {}
    
    def _check_achievement_requirements(self, achievement: Dict[str, Any], 
                                      activity_data: Dict[str, Any], 
                                      student_progress: Dict[str, Any]) -> bool:
        """Check if achievement requirements are met."""
        requirements = achievement.get("requirements", {})
        
        for req_key, req_value in requirements.items():
            if req_key == "questions_asked":
                if student_progress.get("total_questions", 0) < req_value:
                    return False
            elif req_key == "languages_used":
                if len(student_progress.get("languages_used", [])) < req_value:
                    return False
            elif req_key == "study_streak":
                if student_progress.get("current_streak", 0) < req_value:
                    return False
            elif req_key == "modules_completed_daily":
                if activity_data.get("modules_completed_today", 0) < req_value:
                    return False
            elif req_key == "students_helped":
                if student_progress.get("students_helped", 0) < req_value:
                    return False
            elif req_key == "perfect_scores":
                if student_progress.get("perfect_scores", 0) < req_value:
                    return False
            elif req_key == "early_study_days":
                if student_progress.get("early_study_days", 0) < req_value:
                    return False
            elif req_key == "late_study_days":
                if student_progress.get("late_study_days", 0) < req_value:
                    return False
        
        return True
    
    def _get_student_progress(self, student_id: str) -> Dict[str, Any]:
        """Get student progress data (mock implementation)."""
        # In production, this would fetch from database
        return {
            "total_points": 150,
            "total_questions": 25,
            "languages_used": ["en", "am", "om"],
            "current_streak": 3,
            "longest_streak": 7,
            "earned_achievements": ["first_question"],
            "earned_badges": ["bronze_learner"],
            "students_helped": 2,
            "perfect_scores": 1,
            "early_study_days": 2,
            "late_study_days": 1
        }
    
    def _update_student_progress(self, student_id: str, achievement_id: str, points: int):
        """Update student progress with new achievement."""
        # In production, this would update database
        logger.info(f"Student {student_id} earned achievement {achievement_id} for {points} points")
    
    def _update_student_badges(self, student_id: str, badge_id: str):
        """Update student badges."""
        # In production, this would update database
        logger.info(f"Student {student_id} earned badge {badge_id}")
    
    def _check_streak_achievements(self, student_id: str, current_streak: int) -> List[Dict[str, Any]]:
        """Check for streak-related achievements."""
        achievements = []
        
        streak_milestones = [3, 7, 14, 30, 60, 100]
        
        for milestone in streak_milestones:
            if current_streak == milestone:
                achievements.append({
                    "type": "streak_milestone",
                    "milestone": milestone,
                    "message": f"Amazing! {milestone} day streak! 🔥"
                })
        
        return achievements
    
    def _get_next_streak_milestone(self, current_streak: int) -> Optional[int]:
        """Get next streak milestone."""
        milestones = [3, 7, 14, 30, 60, 100]
        
        for milestone in milestones:
            if current_streak < milestone:
                return milestone
        
        return None
    
    def _get_all_students_data(self) -> List[Dict[str, Any]]:
        """Get all students data (mock implementation)."""
        # In production, this would fetch from database
        return [
            {"student_id": "student1", "points": 500, "name": "Alice"},
            {"student_id": "student2", "points": 450, "name": "Bob"},
            {"student_id": "student3", "points": 400, "name": "Charlie"},
            {"student_id": "student4", "points": 350, "name": "Diana"},
            {"student_id": "student5", "points": 300, "name": "Eve"}
        ]
    
    def _filter_by_time_period(self, students: List[Dict[str, Any]], time_period: str) -> List[Dict[str, Any]]:
        """Filter students by time period."""
        # In production, this would filter based on actual time data
        return students
    
    def _get_student_tier(self, points: int) -> str:
        """Get student tier based on points."""
        if points >= 5000:
            return "Diamond"
        elif points >= 2500:
            return "Platinum"
        elif points >= 1000:
            return "Gold"
        elif points >= 500:
            return "Silver"
        else:
            return "Bronze"
    
    def _get_challenge_name(self, challenge_type: str) -> str:
        """Get challenge name based on type."""
        names = {
            "study_streak": "Study Streak Challenge",
            "language_exploration": "Language Explorer Challenge",
            "question_master": "Question Master Challenge",
            "helpful_peer": "Helpful Peer Challenge"
        }
        return names.get(challenge_type, "Learning Challenge")
    
    def _get_challenge_description(self, challenge_type: str) -> str:
        """Get challenge description based on type."""
        descriptions = {
            "study_streak": "Maintain a study streak for the challenge duration",
            "language_exploration": "Use all 6 supported languages during the challenge",
            "question_master": "Ask a certain number of questions during the challenge",
            "helpful_peer": "Help other students during the challenge period"
        }
        return descriptions.get(challenge_type, "Complete the challenge requirements")
    
    def _get_challenge_rewards(self, challenge_type: str) -> Dict[str, Any]:
        """Get challenge rewards based on type."""
        rewards = {
            "study_streak": {"points": 100, "badge": "streak_champion"},
            "language_exploration": {"points": 150, "badge": "polyglot"},
            "question_master": {"points": 200, "badge": "curious_mind"},
            "helpful_peer": {"points": 175, "badge": "community_helper"}
        }
        return rewards.get(challenge_type, {"points": 50, "badge": "challenge_completer"})
