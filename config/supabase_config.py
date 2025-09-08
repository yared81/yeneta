"""
Supabase Configuration for Yeneta Platform
Handles authentication, database operations, and real-time features
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import streamlit as st

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    st.warning("Supabase not available. Install: pip install supabase")

class SupabaseConfig:
    """Supabase configuration and database operations"""
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL", "your-supabase-url")
        self.key = os.getenv("SUPABASE_ANON_KEY", "your-supabase-anon-key")
        self.client = None
        
        if SUPABASE_AVAILABLE and self.url != "your-supabase-url":
            try:
                self.client = create_client(self.url, self.key)
            except Exception as e:
                st.error(f"Failed to connect to Supabase: {e}")
    
    def is_connected(self) -> bool:
        """Check if Supabase is connected"""
        return self.client is not None
    
    def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        """Authenticate user with email and password"""
        if not self.is_connected():
            return {"success": False, "error": "Supabase not connected"}
        
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                return {
                    "success": True,
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email,
                        "created_at": response.user.created_at
                    },
                    "session": response.session
                }
            else:
                return {"success": False, "error": "Invalid credentials"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_user(self, email: str, password: str, full_name: str) -> Dict[str, Any]:
        """Create new user account"""
        if not self.is_connected():
            return {"success": False, "error": "Supabase not connected"}
        
        try:
            response = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": full_name
                    }
                }
            })
            
            if response.user:
                # Insert user profile
                profile_data = {
                    "id": response.user.id,
                    "email": email,
                    "full_name": full_name,
                    "preferred_language": "en",
                    "learning_level": "beginner",
                    "created_at": datetime.now().isoformat()
                }
                
                self.client.table("users").insert(profile_data).execute()
                
                return {
                    "success": True,
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email,
                        "full_name": full_name
                    }
                }
            else:
                return {"success": False, "error": "Failed to create user"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile data"""
        if not self.is_connected():
            return {"success": False, "error": "Supabase not connected"}
        
        try:
            response = self.client.table("users").select("*").eq("id", user_id).execute()
            
            if response.data:
                return {"success": True, "profile": response.data[0]}
            else:
                return {"success": False, "error": "User not found"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update_user_profile(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile"""
        if not self.is_connected():
            return {"success": False, "error": "Supabase not connected"}
        
        try:
            response = self.client.table("users").update(updates).eq("id", user_id).execute()
            return {"success": True, "data": response.data}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_conversation(self, user_id: str, title: str, language: str = "en") -> Dict[str, Any]:
        """Create new conversation"""
        if not self.is_connected():
            return {"success": False, "error": "Supabase not connected"}
        
        try:
            conversation_data = {
                "user_id": user_id,
                "title": title,
                "language": language,
                "created_at": datetime.now().isoformat()
            }
            
            response = self.client.table("conversations").insert(conversation_data).execute()
            return {"success": True, "conversation": response.data[0]}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def add_message(self, conversation_id: str, user_id: str, role: str, content: str, language: str = "en") -> Dict[str, Any]:
        """Add message to conversation"""
        if not self.is_connected():
            return {"success": False, "error": "Supabase not connected"}
        
        try:
            message_data = {
                "conversation_id": conversation_id,
                "user_id": user_id,
                "role": role,
                "content": content,
                "language": language,
                "created_at": datetime.now().isoformat()
            }
            
            response = self.client.table("messages").insert(message_data).execute()
            return {"success": True, "message": response.data[0]}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_conversation_messages(self, conversation_id: str) -> Dict[str, Any]:
        """Get all messages for a conversation"""
        if not self.is_connected():
            return {"success": False, "error": "Supabase not connected"}
        
        try:
            response = self.client.table("messages").select("*").eq("conversation_id", conversation_id).order("created_at").execute()
            return {"success": True, "messages": response.data}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_user_conversations(self, user_id: str) -> Dict[str, Any]:
        """Get all conversations for a user"""
        if not self.is_connected():
            return {"success": False, "error": "Supabase not connected"}
        
        try:
            response = self.client.table("conversations").select("*").eq("user_id", user_id).order("updated_at", desc=True).execute()
            return {"success": True, "conversations": response.data}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update_learning_progress(self, user_id: str, subject: str, topic: str, proficiency_level: int) -> Dict[str, Any]:
        """Update user learning progress"""
        if not self.is_connected():
            return {"success": False, "error": "Supabase not connected"}
        
        try:
            # Check if progress record exists
            existing = self.client.table("learning_progress").select("*").eq("user_id", user_id).eq("subject", subject).eq("topic", topic).execute()
            
            if existing.data:
                # Update existing record
                response = self.client.table("learning_progress").update({
                    "proficiency_level": proficiency_level,
                    "updated_at": datetime.now().isoformat()
                }).eq("user_id", user_id).eq("subject", subject).eq("topic", topic).execute()
            else:
                # Create new record
                progress_data = {
                    "user_id": user_id,
                    "subject": subject,
                    "topic": topic,
                    "proficiency_level": proficiency_level,
                    "created_at": datetime.now().isoformat()
                }
                response = self.client.table("learning_progress").insert(progress_data).execute()
            
            return {"success": True, "data": response.data}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_user_dashboard(self, user_id: str) -> Dict[str, Any]:
        """Get user dashboard data"""
        if not self.is_connected():
            return {"success": False, "error": "Supabase not connected"}
        
        try:
            # Get user stats
            response = self.client.rpc("get_user_dashboard", {"user_uuid": user_id}).execute()
            return {"success": True, "dashboard": response.data}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def add_achievement(self, user_id: str, achievement_type: str, achievement_name: str, description: str, points: int = 0) -> Dict[str, Any]:
        """Add user achievement"""
        if not self.is_connected():
            return {"success": False, "error": "Supabase not connected"}
        
        try:
            achievement_data = {
                "user_id": user_id,
                "achievement_type": achievement_type,
                "achievement_name": achievement_name,
                "description": description,
                "points": points,
                "earned_at": datetime.now().isoformat()
            }
            
            response = self.client.table("user_achievements").insert(achievement_data).execute()
            return {"success": True, "achievement": response.data[0]}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def log_analytics_event(self, user_id: str, event_type: str, event_data: Dict[str, Any], session_id: str = None) -> Dict[str, Any]:
        """Log analytics event"""
        if not self.is_connected():
            return {"success": False, "error": "Supabase not connected"}
        
        try:
            event_data_record = {
                "user_id": user_id,
                "event_type": event_type,
                "event_data": event_data,
                "session_id": session_id,
                "created_at": datetime.now().isoformat()
            }
            
            response = self.client.table("analytics_events").insert(event_data_record).execute()
            return {"success": True, "event": response.data[0]}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
