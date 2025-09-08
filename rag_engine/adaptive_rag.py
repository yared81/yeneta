"""
🎯 Adaptive RAG Engine
Learning level-based response adaptation

This module implements:
- Beginner/Intermediate/Advanced response complexity
- Adaptive prompt engineering
- Learning progression tracking
- Difficulty-based content filtering
"""

import os
from typing import Dict, List, Optional, Tuple
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

class AdaptiveRAGEngine:
    """
    Adaptive RAG engine that adjusts response complexity based on learning level
    Implements progressive learning with appropriate scaffolding
    """
    
    def __init__(self):
        self.learning_levels = {
            "beginner": {
                "name": "Beginner",
                "icon": "🌱",
                "description": "Simple explanations with step-by-step guidance",
                "complexity": 1,
                "max_sentence_length": 15,
                "use_examples": True,
                "use_analogies": True,
                "scaffolding": True
            },
            "intermediate": {
                "name": "Intermediate", 
                "icon": "🌿",
                "description": "Balanced complexity with examples and reasoning",
                "complexity": 2,
                "max_sentence_length": 25,
                "use_examples": True,
                "use_analogies": False,
                "scaffolding": False
            },
            "advanced": {
                "name": "Advanced",
                "icon": "🌳", 
                "description": "Complex reasoning with minimal hand-holding",
                "complexity": 3,
                "max_sentence_length": 40,
                "use_examples": False,
                "use_analogies": False,
                "scaffolding": False
            }
        }
        
        # Initialize Groq LLM
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.1,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        # Learning progression tracking
        self.user_progress = {}
    
    def generate_response(
        self, 
        query: str, 
        language: str = "en",
        level: str = "beginner",
        context: str = ""
    ) -> str:
        """
        Generate adaptive response based on learning level
        """
        level_config = self.learning_levels.get(level, self.learning_levels["beginner"])
        
        # Get appropriate prompt template
        prompt_template = self._get_adaptive_prompt(level, language)
        
        # Create the prompt
        prompt = ChatPromptTemplate.from_template(prompt_template)
        
        # Build the chain
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            response = chain.invoke({
                "query": query,
                "context": context,
                "level": level_config["name"],
                "complexity": level_config["complexity"],
                "max_length": level_config["max_sentence_length"],
                "use_examples": level_config["use_examples"],
                "use_analogies": level_config["use_analogies"],
                "scaffolding": level_config["scaffolding"]
            })
            
            # Post-process based on level
            processed_response = self._post_process_response(response, level_config)
            
            # Track learning progress
            self._track_progress(query, level, language)
            
            return processed_response
            
        except Exception as e:
            st.error(f"Error generating adaptive response: {e}")
            return f"Sorry, I encountered an error while processing your question at the {level} level."
    
    def _get_adaptive_prompt(self, level: str, language: str) -> str:
        """Get adaptive prompt template based on level and language"""
        
        base_prompt = """
        You are Yeneta, an AI study assistant. You must adapt your response to the {level} learning level.
        
        Learning Level: {level} (Complexity: {complexity}/3)
        Context: {context}
        Question: {query}
        
        Response Guidelines:
        - Maximum sentence length: {max_length} words
        - Use examples: {use_examples}
        - Use analogies: {use_analogies}
        - Provide scaffolding: {scaffolding}
        
        """
        
        if level == "beginner":
            return base_prompt + """
            BEGINNER RESPONSE REQUIREMENTS:
            1. Start with simple, clear explanations
            2. Break complex concepts into small steps
            3. Use everyday analogies and examples
            4. Provide step-by-step guidance
            5. Use encouraging, supportive language
            6. Ask if they need clarification
            7. Avoid jargon and technical terms
            8. Keep sentences short and simple
            
            Example structure:
            - "Let me explain this step by step..."
            - "Think of it like..."
            - "Here's a simple way to understand..."
            - "Does this make sense so far?"
            """
        
        elif level == "intermediate":
            return base_prompt + """
            INTERMEDIATE RESPONSE REQUIREMENTS:
            1. Provide balanced explanations with some complexity
            2. Include relevant examples and applications
            3. Show connections between concepts
            4. Use appropriate technical terms with explanations
            5. Encourage critical thinking
            6. Provide reasoning behind answers
            7. Suggest related topics for deeper learning
            
            Example structure:
            - "Here's how this works..."
            - "This connects to..."
            - "An important consideration is..."
            - "You might also want to explore..."
            """
        
        else:  # advanced
            return base_prompt + """
            ADVANCED RESPONSE REQUIREMENTS:
            1. Provide sophisticated, nuanced explanations
            2. Include complex reasoning and analysis
            3. Reference advanced concepts and theories
            4. Use technical terminology appropriately
            5. Encourage independent thinking and research
            6. Provide multiple perspectives when relevant
            7. Suggest advanced applications and extensions
            
            Example structure:
            - "From an advanced perspective..."
            - "The underlying mechanism involves..."
            - "This raises interesting questions about..."
            - "For further exploration, consider..."
            """
    
    def _post_process_response(self, response: str, level_config: Dict) -> str:
        """Post-process response based on learning level"""
        
        if level_config["complexity"] == 1:  # Beginner
            # Ensure simple language
            response = self._simplify_language(response)
            # Add encouraging elements
            response = self._add_encouragement(response)
            # Add scaffolding questions
            response = self._add_scaffolding(response)
            
        elif level_config["complexity"] == 2:  # Intermediate
            # Balance complexity
            response = self._balance_complexity(response)
            # Add connections
            response = self._add_connections(response)
            
        else:  # Advanced
            # Ensure sophisticated language
            response = self._enhance_complexity(response)
            # Add advanced insights
            response = self._add_advanced_insights(response)
        
        return response
    
    def _simplify_language(self, text: str) -> str:
        """Simplify language for beginners"""
        # Replace complex words with simpler alternatives
        replacements = {
            "utilize": "use",
            "facilitate": "help",
            "implement": "do",
            "comprehensive": "complete",
            "sophisticated": "advanced",
            "paradigm": "way of thinking",
            "methodology": "method"
        }
        
        for complex_word, simple_word in replacements.items():
            text = text.replace(complex_word, simple_word)
        
        return text
    
    def _add_encouragement(self, text: str) -> str:
        """Add encouraging elements for beginners"""
        encouragements = [
            "Great question!",
            "You're doing well!",
            "Keep up the good work!",
            "That's a smart way to think about it!",
            "You're on the right track!"
        ]
        
        # Add encouragement at the beginning
        import random
        encouragement = random.choice(encouragements)
        return f"{encouragement} {text}"
    
    def _add_scaffolding(self, text: str) -> str:
        """Add scaffolding questions for beginners"""
        scaffolding_questions = [
            "Does this make sense so far?",
            "Would you like me to explain any part in more detail?",
            "Do you have any questions about this?",
            "Is there anything you'd like me to clarify?"
        ]
        
        import random
        question = random.choice(scaffolding_questions)
        return f"{text}\n\n{question}"
    
    def _balance_complexity(self, text: str) -> str:
        """Balance complexity for intermediate learners"""
        # Add transitional phrases
        transitions = [
            "Furthermore,",
            "Additionally,",
            "Moreover,",
            "It's also important to note that",
            "Another key point is"
        ]
        
        # This is a simplified version - in practice, you'd use more sophisticated NLP
        return text
    
    def _add_connections(self, text: str) -> str:
        """Add connections between concepts for intermediate learners"""
        connection_phrases = [
            "This relates to",
            "This connects to",
            "This is similar to",
            "This builds on"
        ]
        
        # Simplified connection addition
        return text
    
    def _enhance_complexity(self, text: str) -> str:
        """Enhance complexity for advanced learners"""
        # Add sophisticated vocabulary
        enhancements = {
            "good": "excellent",
            "important": "crucial",
            "big": "significant",
            "small": "minimal",
            "easy": "straightforward"
        }
        
        for simple_word, complex_word in enhancements.items():
            text = text.replace(simple_word, complex_word)
        
        return text
    
    def _add_advanced_insights(self, text: str) -> str:
        """Add advanced insights for advanced learners"""
        insight_phrases = [
            "From a theoretical perspective,",
            "The underlying mechanism involves",
            "This raises interesting questions about",
            "The implications of this are"
        ]
        
        # Simplified insight addition
        return text
    
    def _track_progress(self, query: str, level: str, language: str):
        """Track user's learning progress"""
        # This would integrate with a database to track progress
        # For now, we'll use session state
        if "learning_progress" not in st.session_state:
            st.session_state.learning_progress = {}
        
        progress_key = f"{level}_{language}"
        if progress_key not in st.session_state.learning_progress:
            st.session_state.learning_progress[progress_key] = {
                "questions_asked": 0,
                "topics_covered": set(),
                "difficulty_progression": []
            }
        
        st.session_state.learning_progress[progress_key]["questions_asked"] += 1
        
        # Extract topics (simplified)
        topics = self._extract_topics(query)
        st.session_state.learning_progress[progress_key]["topics_covered"].update(topics)
    
    def _extract_topics(self, query: str) -> List[str]:
        """Extract topics from query (simplified implementation)"""
        # This would use more sophisticated NLP in practice
        common_topics = [
            "mathematics", "science", "history", "literature", 
            "language", "geography", "biology", "chemistry",
            "physics", "art", "music", "sports"
        ]
        
        topics = []
        query_lower = query.lower()
        for topic in common_topics:
            if topic in query_lower:
                topics.append(topic)
        
        return topics
    
    def suggest_level_progression(self, user_id: str) -> Optional[str]:
        """Suggest when user should progress to next level"""
        if "learning_progress" not in st.session_state:
            return None
        
        # Simple progression logic
        for level_key, progress in st.session_state.learning_progress.items():
            if progress["questions_asked"] >= 10:  # Threshold for progression
                current_level = level_key.split("_")[0]
                if current_level == "beginner":
                    return "intermediate"
                elif current_level == "intermediate":
                    return "advanced"
        
        return None
    
    def get_learning_analytics(self) -> Dict:
        """Get learning analytics for the user"""
        if "learning_progress" not in st.session_state:
            return {}
        
        analytics = {}
        for level_key, progress in st.session_state.learning_progress.items():
            level, language = level_key.split("_")
            analytics[level_key] = {
                "level": level,
                "language": language,
                "questions_asked": progress["questions_asked"],
                "topics_covered": len(progress["topics_covered"]),
                "topics_list": list(progress["topics_covered"])
            }
        
        return analytics
    
    def get_level_info(self, level: str) -> Dict:
        """Get information about a specific learning level"""
        return self.learning_levels.get(level, self.learning_levels["beginner"])
    
    def get_all_levels(self) -> Dict:
        """Get all available learning levels"""
        return self.learning_levels
