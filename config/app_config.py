"""
🔧 Application Configuration
Centralized configuration management for Yeneta platform
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AppConfig:
    """
    Centralized configuration class for Yeneta platform
    Manages all application settings and environment variables
    """
    
    def __init__(self):
        # API Configuration
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
        self.SUPABASE_URL = os.getenv("SUPABASE_URL", "")
        self.SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
        
        # Application Settings
        self.APP_NAME = os.getenv("APP_NAME", "Yeneta")
        self.APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
        self.DEBUG = os.getenv("DEBUG", "True").lower() == "true"
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        
        # RAG Configuration
        self.EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        self.CROSS_ENCODER_MODEL = os.getenv("CROSS_ENCODER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")
        self.CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_store")
        
        # Language Configuration
        self.SUPPORTED_LANGUAGES = os.getenv("SUPPORTED_LANGUAGES", "am,om,ti,en,yo,sw").split(",")
        self.DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
        
        # Voice Configuration
        self.VOICE_ENABLED = os.getenv("VOICE_ENABLED", "True").lower() == "true"
        self.TTS_LANGUAGE = os.getenv("TTS_LANGUAGE", "en")
        self.STT_LANGUAGE = os.getenv("STT_LANGUAGE", "en")
        
        # File Upload Configuration
        self.MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
        self.ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", "pdf,docx,txt,md").split(",")
        
        # Cache Configuration
        self.REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))
        
        # Security Configuration
        self.SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
        self.JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret_here")
        
        # Monitoring Configuration
        self.SENTRY_DSN = os.getenv("SENTRY_DSN", "")
        
        # Initialize language mappings
        self._init_language_mappings()
        
        # Initialize RAG settings
        self._init_rag_settings()
    
    def _init_language_mappings(self):
        """Initialize language mappings and configurations"""
        self.LANGUAGE_MAPPINGS = {
            "en": {
                "name": "English",
                "native_name": "English",
                "country": "Universal",
                "flag": "🇺🇸",
                "code": "en",
                "rtl": False
            },
            "am": {
                "name": "Amharic",
                "native_name": "አማርኛ", 
                "country": "Ethiopia",
                "flag": "🇪🇹",
                "code": "am",
                "rtl": False
            },
            "om": {
                "name": "Afaan Oromo",
                "native_name": "Afaan Oromoo",
                "country": "Ethiopia", 
                "flag": "🇪🇹",
                "code": "om",
                "rtl": False
            },
            "ti": {
                "name": "Tigrigna",
                "native_name": "ትግርኛ",
                "country": "Ethiopia/Eritrea",
                "flag": "🇪🇹", 
                "code": "ti",
                "rtl": False
            },
            "yo": {
                "name": "Yoruba",
                "native_name": "Èdè Yorùbá",
                "country": "Nigeria",
                "flag": "🇳🇬",
                "code": "yo", 
                "rtl": False
            },
            "sw": {
                "name": "Swahili",
                "native_name": "Kiswahili",
                "country": "East Africa",
                "flag": "🇰🇪",
                "code": "sw",
                "rtl": False
            }
        }
    
    def _init_rag_settings(self):
        """Initialize RAG-specific settings"""
        self.RAG_SETTINGS = {
            "chunk_size": 1000,
            "chunk_overlap": 100,
            "search_k": 10,
            "reranker_top_n": 3,
            "temperature": 0.1,
            "max_tokens": 2048,
            "timeout": 30
        }
        
        self.LEARNING_LEVELS = {
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
    
    def get_language_info(self, lang_code: str) -> Dict:
        """Get language information by code"""
        return self.LANGUAGE_MAPPINGS.get(lang_code, self.LANGUAGE_MAPPINGS["en"])
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported language codes"""
        return self.SUPPORTED_LANGUAGES
    
    def is_language_supported(self, lang_code: str) -> bool:
        """Check if language is supported"""
        return lang_code in self.SUPPORTED_LANGUAGES
    
    def get_learning_level_info(self, level: str) -> Dict:
        """Get learning level information"""
        return self.LEARNING_LEVELS.get(level, self.LEARNING_LEVELS["beginner"])
    
    def get_rag_setting(self, setting_name: str, default=None):
        """Get RAG setting value"""
        return self.RAG_SETTINGS.get(setting_name, default)
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return any issues"""
        issues = []
        
        # Check required API keys
        if not self.GROQ_API_KEY:
            issues.append("GROQ_API_KEY is required")
        
        # Check Supabase configuration
        if not self.SUPABASE_URL:
            issues.append("SUPABASE_URL is required")
        
        if not self.SUPABASE_KEY:
            issues.append("SUPABASE_KEY is required")
        
        # Check file upload settings
        if self.MAX_FILE_SIZE <= 0:
            issues.append("MAX_FILE_SIZE must be positive")
        
        if not self.ALLOWED_EXTENSIONS:
            issues.append("ALLOWED_EXTENSIONS cannot be empty")
        
        # Check language settings
        for lang in self.SUPPORTED_LANGUAGES:
            if lang not in self.LANGUAGE_MAPPINGS:
                issues.append(f"Language {lang} not found in mappings")
        
        return issues
    
    def get_config_summary(self) -> Dict:
        """Get configuration summary for debugging"""
        return {
            "app_name": self.APP_NAME,
            "app_version": self.APP_VERSION,
            "debug": self.DEBUG,
            "supported_languages": len(self.SUPPORTED_LANGUAGES),
            "voice_enabled": self.VOICE_ENABLED,
            "max_file_size": self.MAX_FILE_SIZE,
            "rag_settings": self.RAG_SETTINGS,
            "validation_issues": self.validate_config()
        }
    
    def update_setting(self, setting_name: str, value: str):
        """Update a configuration setting"""
        if hasattr(self, setting_name.upper()):
            setattr(self, setting_name.upper(), value)
        else:
            raise ValueError(f"Unknown setting: {setting_name}")
    
    def export_config(self) -> Dict:
        """Export configuration as dictionary"""
        return {
            "app_name": self.APP_NAME,
            "app_version": self.APP_VERSION,
            "debug": self.DEBUG,
            "log_level": self.LOG_LEVEL,
            "supported_languages": self.SUPPORTED_LANGUAGES,
            "default_language": self.DEFAULT_LANGUAGE,
            "voice_enabled": self.VOICE_ENABLED,
            "max_file_size": self.MAX_FILE_SIZE,
            "allowed_extensions": self.ALLOWED_EXTENSIONS,
            "rag_settings": self.RAG_SETTINGS,
            "learning_levels": self.LEARNING_LEVELS
        }
