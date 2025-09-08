"""
🧠 Memory-Augmented RAG Engine
Personalized learning with persistent memory

This module implements:
- Session memory for context awareness
- Long-term learning progress tracking
- Personalized response generation
- Weak topic identification and reinforcement
- Learning pattern analysis
"""

import os
import json
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

class MemoryAugmentedRAG:
    """
    Memory-Augmented RAG engine that personalizes responses based on user history
    Implements both short-term session memory and long-term learning memory
    """
    
    def __init__(self):
        # Initialize Groq LLM
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.1,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        # Memory configuration
        self.memory_config = {
            "session_memory_size": 20,  # Last 20 interactions
            "long_term_memory_size": 1000,  # Last 1000 interactions
            "weak_topic_threshold": 3,  # Topics with <3 correct answers
            "strong_topic_threshold": 8,  # Topics with >8 correct answers
            "memory_decay_days": 30  # Memory decay after 30 days
        }
        
        # Initialize memory structures
        self._init_memory_structures()
    
    def _init_memory_structures(self):
        """Initialize memory structures in session state"""
        if "memory_rag" not in st.session_state:
            st.session_state.memory_rag = {
                "session_memory": [],
                "long_term_memory": [],
                "learning_profile": {
                    "weak_topics": {},
                    "strong_topics": {},
                    "learning_patterns": {},
                    "preferred_language": "en",
                    "preferred_level": "beginner",
                    "total_interactions": 0,
                    "last_updated": datetime.now().isoformat()
                },
                "topic_mastery": {},
                "interaction_history": []
            }
    
    def personalize_response(
        self, 
        response: str, 
        user_history: List[Dict],
        language: str = "en",
        learning_level: str = "beginner"
    ) -> str:
        """
        Personalize response based on user's learning history and patterns
        """
        try:
            # Update memory with current interaction
            self._update_memory(user_history, language, learning_level)
            
            # Analyze learning patterns
            learning_analysis = self._analyze_learning_patterns()
            
            # Identify weak topics
            weak_topics = self._identify_weak_topics()
            
            # Generate personalized response
            personalized_response = self._generate_personalized_response(
                response, learning_analysis, weak_topics, language, learning_level
            )
            
            # Update learning profile
            self._update_learning_profile(learning_analysis, weak_topics)
            
            return personalized_response
            
        except Exception as e:
            st.error(f"Error in memory-augmented personalization: {e}")
            return response
    
    def _update_memory(self, user_history: List[Dict], language: str, learning_level: str):
        """Update memory with recent interactions"""
        memory = st.session_state.memory_rag
        
        # Add recent interactions to session memory
        recent_interactions = user_history[-self.memory_config["session_memory_size"]:]
        
        for interaction in recent_interactions:
            memory_entry = {
                "timestamp": interaction.get("timestamp", datetime.now().isoformat()),
                "query": interaction.get("content", ""),
                "response": interaction.get("content", ""),
                "language": language,
                "learning_level": learning_level,
                "topics": self._extract_topics(interaction.get("content", "")),
                "interaction_type": interaction.get("role", "user")
            }
            
            memory["session_memory"].append(memory_entry)
            memory["interaction_history"].append(memory_entry)
        
        # Keep session memory within limits
        if len(memory["session_memory"]) > self.memory_config["session_memory_size"]:
            memory["session_memory"] = memory["session_memory"][-self.memory_config["session_memory_size"]:]
        
        # Update long-term memory
        memory["long_term_memory"] = memory["interaction_history"][-self.memory_config["long_term_memory_size"]:]
        
        # Update total interactions
        memory["learning_profile"]["total_interactions"] = len(memory["interaction_history"])
        memory["learning_profile"]["last_updated"] = datetime.now().isoformat()
    
    def _analyze_learning_patterns(self) -> Dict:
        """Analyze user's learning patterns and preferences"""
        memory = st.session_state.memory_rag
        interactions = memory["interaction_history"]
        
        if not interactions:
            return {"patterns": {}, "preferences": {}}
        
        # Analyze language preferences
        language_counts = {}
        level_counts = {}
        topic_counts = {}
        time_patterns = {}
        
        for interaction in interactions:
            # Language analysis
            lang = interaction.get("language", "en")
            language_counts[lang] = language_counts.get(lang, 0) + 1
            
            # Level analysis
            level = interaction.get("learning_level", "beginner")
            level_counts[level] = level_counts.get(level, 0) + 1
            
            # Topic analysis
            topics = interaction.get("topics", [])
            for topic in topics:
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
            
            # Time pattern analysis
            try:
                timestamp = datetime.fromisoformat(interaction["timestamp"])
                hour = timestamp.hour
                time_patterns[hour] = time_patterns.get(hour, 0) + 1
            except:
                pass
        
        # Determine preferences
        preferred_language = max(language_counts.items(), key=lambda x: x[1])[0] if language_counts else "en"
        preferred_level = max(level_counts.items(), key=lambda x: x[1])[0] if level_counts else "beginner"
        most_active_hour = max(time_patterns.items(), key=lambda x: x[1])[0] if time_patterns else 12
        
        return {
            "preferred_language": preferred_language,
            "preferred_level": preferred_level,
            "most_active_hour": most_active_hour,
            "language_distribution": language_counts,
            "level_distribution": level_counts,
            "topic_frequency": topic_counts,
            "total_interactions": len(interactions)
        }
    
    def _identify_weak_topics(self) -> List[str]:
        """Identify topics where user needs more practice"""
        memory = st.session_state.memory_rag
        topic_mastery = memory["topic_mastery"]
        
        weak_topics = []
        for topic, mastery_data in topic_mastery.items():
            correct_answers = mastery_data.get("correct", 0)
            total_attempts = mastery_data.get("total", 0)
            
            if total_attempts > 0:
                accuracy = correct_answers / total_attempts
                if accuracy < 0.6 or total_attempts < self.memory_config["weak_topic_threshold"]:
                    weak_topics.append(topic)
        
        return weak_topics
    
    def _generate_personalized_response(
        self, 
        base_response: str,
        learning_analysis: Dict,
        weak_topics: List[str],
        language: str,
        learning_level: str
    ) -> str:
        """Generate personalized response based on learning analysis"""
        
        # Build personalization context
        personalization_context = self._build_personalization_context(
            learning_analysis, weak_topics, language, learning_level
        )
        
        prompt_template = """
        You are personalizing an educational response based on the user's learning profile.
        
        Base Response: {base_response}
        
        Personalization Context:
        {personalization_context}
        
        Personalize the response by:
        1. Addressing weak topics if relevant
        2. Using preferred learning style
        3. Building on previous knowledge
        4. Providing encouragement based on progress
        5. Suggesting related topics for improvement
        
        Keep the core educational content but make it more personalized and relevant.
        """
        
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            personalized_response = chain.invoke({
                "base_response": base_response,
                "personalization_context": personalization_context
            })
            
            return personalized_response.strip()
            
        except Exception as e:
            st.warning(f"Personalization failed: {e}")
            return base_response
    
    def _build_personalization_context(
        self, 
        learning_analysis: Dict, 
        weak_topics: List[str], 
        language: str, 
        learning_level: str
    ) -> str:
        """Build context for personalization"""
        
        context_parts = []
        
        # Learning preferences
        context_parts.append(f"Learning Preferences:")
        context_parts.append(f"- Preferred Language: {learning_analysis.get('preferred_language', language)}")
        context_parts.append(f"- Preferred Level: {learning_analysis.get('preferred_level', learning_level)}")
        context_parts.append(f"- Total Interactions: {learning_analysis.get('total_interactions', 0)}")
        
        # Weak topics
        if weak_topics:
            context_parts.append(f"Weak Topics (need more practice): {', '.join(weak_topics)}")
        
        # Topic frequency
        topic_frequency = learning_analysis.get("topic_frequency", {})
        if topic_frequency:
            top_topics = sorted(topic_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
            context_parts.append(f"Most Studied Topics: {', '.join([f'{topic}({count})' for topic, count in top_topics])}")
        
        # Learning patterns
        context_parts.append(f"Learning Patterns:")
        context_parts.append(f"- Most Active Hour: {learning_analysis.get('most_active_hour', 12)}:00")
        
        return "\n".join(context_parts)
    
    def _update_learning_profile(self, learning_analysis: Dict, weak_topics: List[str]):
        """Update user's learning profile"""
        memory = st.session_state.memory_rag
        profile = memory["learning_profile"]
        
        # Update preferences
        profile["preferred_language"] = learning_analysis.get("preferred_language", profile["preferred_language"])
        profile["preferred_level"] = learning_analysis.get("preferred_level", profile["preferred_level"])
        
        # Update weak topics
        for topic in weak_topics:
            profile["weak_topics"][topic] = profile["weak_topics"].get(topic, 0) + 1
        
        # Update strong topics
        topic_frequency = learning_analysis.get("topic_frequency", {})
        for topic, count in topic_frequency.items():
            if count >= self.memory_config["strong_topic_threshold"]:
                profile["strong_topics"][topic] = count
        
        # Update learning patterns
        profile["learning_patterns"] = {
            "language_distribution": learning_analysis.get("language_distribution", {}),
            "level_distribution": learning_analysis.get("level_distribution", {}),
            "most_active_hour": learning_analysis.get("most_active_hour", 12),
            "total_interactions": learning_analysis.get("total_interactions", 0)
        }
        
        profile["last_updated"] = datetime.now().isoformat()
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from text (simplified implementation)"""
        # This would use more sophisticated NLP in practice
        common_topics = [
            "mathematics", "algebra", "geometry", "calculus",
            "science", "biology", "chemistry", "physics",
            "history", "geography", "literature", "language",
            "art", "music", "sports", "technology"
        ]
        
        topics = []
        text_lower = text.lower()
        
        for topic in common_topics:
            if topic in text_lower:
                topics.append(topic)
        
        return topics
    
    def get_learning_insights(self) -> Dict:
        """Get comprehensive learning insights"""
        memory = st.session_state.memory_rag
        
        return {
            "learning_profile": memory["learning_profile"],
            "session_summary": {
                "recent_interactions": len(memory["session_memory"]),
                "total_interactions": len(memory["interaction_history"]),
                "weak_topics_count": len(memory["learning_profile"]["weak_topics"]),
                "strong_topics_count": len(memory["learning_profile"]["strong_topics"])
            },
            "recommendations": self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate personalized learning recommendations"""
        memory = st.session_state.memory_rag
        profile = memory["learning_profile"]
        recommendations = []
        
        # Weak topic recommendations
        weak_topics = list(profile["weak_topics"].keys())
        if weak_topics:
            recommendations.append(f"Focus on improving these weak topics: {', '.join(weak_topics[:3])}")
        
        # Language recommendations
        if profile["preferred_language"] != "en":
            recommendations.append(f"Continue practicing in {profile['preferred_language']} for better comprehension")
        
        # Level progression recommendations
        if profile["total_interactions"] > 20 and profile["preferred_level"] == "beginner":
            recommendations.append("Consider progressing to intermediate level for more challenging content")
        
        # Study time recommendations
        most_active_hour = profile["learning_patterns"].get("most_active_hour", 12)
        recommendations.append(f"Your most productive study time is around {most_active_hour}:00")
        
        return recommendations
    
    def update_topic_mastery(self, topic: str, correct: bool):
        """Update mastery level for a specific topic"""
        memory = st.session_state.memory_rag
        
        if topic not in memory["topic_mastery"]:
            memory["topic_mastery"][topic] = {"correct": 0, "total": 0}
        
        memory["topic_mastery"][topic]["total"] += 1
        if correct:
            memory["topic_mastery"][topic]["correct"] += 1
    
    def get_topic_mastery(self, topic: str) -> Dict:
        """Get mastery level for a specific topic"""
        memory = st.session_state.memory_rag
        
        if topic not in memory["topic_mastery"]:
            return {"correct": 0, "total": 0, "accuracy": 0.0}
        
        mastery_data = memory["topic_mastery"][topic]
        accuracy = mastery_data["correct"] / mastery_data["total"] if mastery_data["total"] > 0 else 0.0
        
        return {
            "correct": mastery_data["correct"],
            "total": mastery_data["total"],
            "accuracy": accuracy
        }
    
    def clear_memory(self, memory_type: str = "session"):
        """Clear specific memory type"""
        memory = st.session_state.memory_rag
        
        if memory_type == "session":
            memory["session_memory"] = []
        elif memory_type == "long_term":
            memory["long_term_memory"] = []
            memory["interaction_history"] = []
        elif memory_type == "all":
            self._init_memory_structures()
    
    def export_memory(self) -> str:
        """Export memory data as JSON"""
        memory = st.session_state.memory_rag
        return json.dumps(memory, indent=2, default=str)
    
    def import_memory(self, memory_data: str):
        """Import memory data from JSON"""
        try:
            imported_memory = json.loads(memory_data)
            st.session_state.memory_rag = imported_memory
            st.success("Memory imported successfully!")
        except Exception as e:
            st.error(f"Failed to import memory: {e}")
