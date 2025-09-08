"""
Yeneta Features Package

This package contains additional features for the Yeneta platform:
- Voice processing for accessibility
- Progress tracking and analytics
- Quiz generation
- File upload and processing
"""

from .voice_processing import VoiceProcessor
from .progress_tracking import ProgressTracker

__all__ = [
    "VoiceProcessor",
    "ProgressTracker"
]
