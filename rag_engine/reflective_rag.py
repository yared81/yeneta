"""
🪞 Self-Reflective RAG Engine
Educational accuracy validation and self-correction

This module implements:
- Response quality validation
- Educational appropriateness checking
- Self-correction mechanisms
- Content safety verification
- Accuracy scoring and improvement
"""

import os
import re
from typing import Dict, List, Optional, Tuple
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

class SelfReflectiveRAG:
    """
    Self-Reflective RAG engine that validates and improves its own responses
    Ensures educational accuracy and appropriateness
    """
    
    def __init__(self):
        # Initialize Groq LLM for validation
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.1,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        # Educational quality criteria
        self.quality_criteria = {
            "accuracy": {
                "weight": 0.3,
                "description": "Factual correctness and precision"
            },
            "clarity": {
                "weight": 0.25,
                "description": "Clear and understandable explanation"
            },
            "completeness": {
                "weight": 0.2,
                "description": "Comprehensive coverage of the topic"
            },
            "appropriateness": {
                "weight": 0.15,
                "description": "Age and context appropriate content"
            },
            "engagement": {
                "weight": 0.1,
                "description": "Encouraging and motivating tone"
            }
        }
        
        # Content safety patterns
        self.safety_patterns = {
            "inappropriate": [
                r"violence", r"harmful", r"dangerous", r"illegal",
                r"discriminatory", r"offensive", r"inappropriate"
            ],
            "misleading": [
                r"always", r"never", r"all", r"none", r"guaranteed",
                r"definitely", r"certainly", r"impossible"
            ]
        }
    
    def validate_response(
        self, 
        response: str, 
        context: str = "",
        language: str = "en",
        learning_level: str = "beginner"
    ) -> Tuple[str, Dict]:
        """
        Validate and improve response quality
        Returns (improved_response, validation_metrics)
        """
        try:
            # Step 1: Safety check
            safety_score, safety_issues = self._check_safety(response)
            
            # Step 2: Educational quality assessment
            quality_score, quality_issues = self._assess_quality(
                response, context, language, learning_level
            )
            
            # Step 3: Accuracy validation
            accuracy_score, accuracy_issues = self._validate_accuracy(
                response, context
            )
            
            # Step 4: Generate improved response if needed
            if safety_score < 0.8 or quality_score < 0.7 or accuracy_score < 0.7:
                improved_response = self._generate_improved_response(
                    response, context, language, learning_level,
                    safety_issues, quality_issues, accuracy_issues
                )
            else:
                improved_response = response
            
            # Step 5: Final validation
            final_validation = self._final_validation(improved_response)
            
            # Compile metrics
            validation_metrics = {
                "safety_score": safety_score,
                "quality_score": quality_score,
                "accuracy_score": accuracy_score,
                "overall_score": (safety_score + quality_score + accuracy_score) / 3,
                "safety_issues": safety_issues,
                "quality_issues": quality_issues,
                "accuracy_issues": accuracy_issues,
                "improvements_made": improved_response != response,
                "final_validation": final_validation
            }
            
            return improved_response, validation_metrics
            
        except Exception as e:
            st.error(f"Error in self-reflective validation: {e}")
            return response, {"error": str(e)}
    
    def _check_safety(self, response: str) -> Tuple[float, List[str]]:
        """Check response for safety issues"""
        issues = []
        response_lower = response.lower()
        
        # Check for inappropriate content
        for pattern in self.safety_patterns["inappropriate"]:
            if re.search(pattern, response_lower):
                issues.append(f"Potentially inappropriate content: {pattern}")
        
        # Check for misleading statements
        for pattern in self.safety_patterns["misleading"]:
            if re.search(pattern, response_lower):
                issues.append(f"Potentially misleading statement: {pattern}")
        
        # Calculate safety score
        safety_score = max(0, 1 - (len(issues) * 0.2))
        
        return safety_score, issues
    
    def _assess_quality(
        self, 
        response: str, 
        context: str, 
        language: str, 
        learning_level: str
    ) -> Tuple[float, List[str]]:
        """Assess educational quality of response"""
        
        prompt_template = """
        You are an educational quality assessor. Evaluate this response for educational quality.
        
        Response: {response}
        Context: {context}
        Language: {language}
        Learning Level: {learning_level}
        
        Rate each criterion from 1-10:
        1. Accuracy: Is the information factually correct?
        2. Clarity: Is the explanation clear and understandable?
        3. Completeness: Does it adequately cover the topic?
        4. Appropriateness: Is it appropriate for the learning level?
        5. Engagement: Is it encouraging and motivating?
        
        Provide scores and identify any issues that need improvement.
        Format: ACCURACY: X/10, CLARITY: X/10, COMPLETENESS: X/10, APPROPRIATENESS: X/10, ENGAGEMENT: X/10
        Issues: [list any issues]
        """
        
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            assessment = chain.invoke({
                "response": response,
                "context": context,
                "language": language,
                "learning_level": learning_level
            })
            
            # Parse scores from assessment
            scores = self._parse_quality_scores(assessment)
            issues = self._parse_quality_issues(assessment)
            
            # Calculate overall quality score
            quality_score = sum(scores.values()) / len(scores) / 10
            
            return quality_score, issues
            
        except Exception as e:
            st.warning(f"Quality assessment failed: {e}")
            return 0.5, ["Quality assessment failed"]
    
    def _validate_accuracy(self, response: str, context: str) -> Tuple[float, List[str]]:
        """Validate factual accuracy of response"""
        
        prompt_template = """
        You are a fact-checker. Validate the accuracy of this response.
        
        Response: {response}
        Context: {context}
        
        Check for:
        1. Factual accuracy
        2. Logical consistency
        3. Proper citations or sources
        4. No contradictions
        
        Rate accuracy from 1-10 and list any inaccuracies.
        Format: ACCURACY: X/10
        Issues: [list any inaccuracies]
        """
        
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            validation = chain.invoke({
                "response": response,
                "context": context
            })
            
            # Parse accuracy score
            accuracy_score = self._parse_accuracy_score(validation)
            issues = self._parse_accuracy_issues(validation)
            
            return accuracy_score, issues
            
        except Exception as e:
            st.warning(f"Accuracy validation failed: {e}")
            return 0.5, ["Accuracy validation failed"]
    
    def _generate_improved_response(
        self, 
        original_response: str,
        context: str,
        language: str,
        learning_level: str,
        safety_issues: List[str],
        quality_issues: List[str],
        accuracy_issues: List[str]
    ) -> str:
        """Generate improved response based on identified issues"""
        
        prompt_template = """
        You are improving an educational response. Fix the identified issues while maintaining the core message.
        
        Original Response: {original_response}
        Context: {context}
        Language: {language}
        Learning Level: {learning_level}
        
        Issues to Fix:
        Safety Issues: {safety_issues}
        Quality Issues: {quality_issues}
        Accuracy Issues: {accuracy_issues}
        
        Generate an improved response that:
        1. Fixes all identified issues
        2. Maintains educational value
        3. Is appropriate for the learning level
        4. Is clear and engaging
        5. Is factually accurate
        
        Improved Response:
        """
        
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            improved_response = chain.invoke({
                "original_response": original_response,
                "context": context,
                "language": language,
                "learning_level": learning_level,
                "safety_issues": ", ".join(safety_issues),
                "quality_issues": ", ".join(quality_issues),
                "accuracy_issues": ", ".join(accuracy_issues)
            })
            
            return improved_response.strip()
            
        except Exception as e:
            st.warning(f"Response improvement failed: {e}")
            return original_response
    
    def _final_validation(self, response: str) -> Dict:
        """Perform final validation of improved response"""
        
        # Basic checks
        checks = {
            "length_appropriate": 50 <= len(response) <= 2000,
            "no_inappropriate_content": not any(
                re.search(pattern, response.lower()) 
                for pattern in self.safety_patterns["inappropriate"]
            ),
            "has_educational_value": any(
                word in response.lower() 
                for word in ["explain", "understand", "learn", "study", "example"]
            ),
            "encouraging_tone": any(
                word in response.lower() 
                for word in ["good", "great", "excellent", "well done", "keep up"]
            )
        }
        
        return {
            "passed": all(checks.values()),
            "checks": checks,
            "score": sum(checks.values()) / len(checks)
        }
    
    def _parse_quality_scores(self, assessment: str) -> Dict[str, float]:
        """Parse quality scores from assessment text"""
        scores = {}
        
        # Look for score patterns like "ACCURACY: 8/10"
        patterns = {
            "accuracy": r"ACCURACY:\s*(\d+)/10",
            "clarity": r"CLARITY:\s*(\d+)/10", 
            "completeness": r"COMPLETENESS:\s*(\d+)/10",
            "appropriateness": r"APPROPRIATENESS:\s*(\d+)/10",
            "engagement": r"ENGAGEMENT:\s*(\d+)/10"
        }
        
        for criterion, pattern in patterns.items():
            match = re.search(pattern, assessment, re.IGNORECASE)
            if match:
                scores[criterion] = float(match.group(1))
            else:
                scores[criterion] = 5.0  # Default score
        
        return scores
    
    def _parse_quality_issues(self, assessment: str) -> List[str]:
        """Parse quality issues from assessment text"""
        issues = []
        
        # Look for issues section
        if "Issues:" in assessment:
            issues_section = assessment.split("Issues:")[1].strip()
            # Split by common separators
            issues = [issue.strip() for issue in re.split(r'[,;]', issues_section) if issue.strip()]
        
        return issues
    
    def _parse_accuracy_score(self, validation: str) -> float:
        """Parse accuracy score from validation text"""
        match = re.search(r"ACCURACY:\s*(\d+)/10", validation, re.IGNORECASE)
        if match:
            return float(match.group(1)) / 10
        return 0.5  # Default score
    
    def _parse_accuracy_issues(self, validation: str) -> List[str]:
        """Parse accuracy issues from validation text"""
        issues = []
        
        if "Issues:" in validation:
            issues_section = validation.split("Issues:")[1].strip()
            issues = [issue.strip() for issue in re.split(r'[,;]', issues_section) if issue.strip()]
        
        return issues
    
    def get_validation_summary(self, metrics: Dict) -> str:
        """Get a human-readable validation summary"""
        if "error" in metrics:
            return f"❌ Validation Error: {metrics['error']}"
        
        overall_score = metrics.get("overall_score", 0)
        
        if overall_score >= 0.8:
            status = "✅ Excellent"
            color = "green"
        elif overall_score >= 0.6:
            status = "⚠️ Good"
            color = "orange"
        else:
            status = "❌ Needs Improvement"
            color = "red"
        
        summary = f"""
        **{status}** (Score: {overall_score:.2f}/1.0)
        
        - Safety: {metrics.get('safety_score', 0):.2f}/1.0
        - Quality: {metrics.get('quality_score', 0):.2f}/1.0  
        - Accuracy: {metrics.get('accuracy_score', 0):.2f}/1.0
        
        {'✅ Response improved' if metrics.get('improvements_made') else '✅ No improvements needed'}
        """
        
        return summary
    
    def log_validation(self, query: str, response: str, metrics: Dict):
        """Log validation results for analysis"""
        # This would integrate with a logging system
        if "validation_log" not in st.session_state:
            st.session_state.validation_log = []
        
        log_entry = {
            "timestamp": st.session_state.get("current_timestamp", "unknown"),
            "query": query[:100],  # Truncate for storage
            "response_length": len(response),
            "overall_score": metrics.get("overall_score", 0),
            "improvements_made": metrics.get("improvements_made", False),
            "issues_count": len(metrics.get("safety_issues", [])) + 
                          len(metrics.get("quality_issues", [])) + 
                          len(metrics.get("accuracy_issues", []))
        }
        
        st.session_state.validation_log.append(log_entry)
        
        # Keep only last 100 entries
        if len(st.session_state.validation_log) > 100:
            st.session_state.validation_log = st.session_state.validation_log[-100:]
