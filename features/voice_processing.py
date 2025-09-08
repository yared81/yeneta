"""
🎤 Voice Processing Module
Speech-to-text and text-to-speech functionality for accessibility

This module implements:
- Speech recognition in multiple languages
- Text-to-speech synthesis
- Voice command processing
- Accessibility features
"""

import os
import io
import tempfile
from typing import Optional, Dict, List
import streamlit as st

try:
    import speech_recognition as sr
    import pyttsx3
    from gtts import gTTS
    import pygame
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    st.warning("Voice processing libraries not available. Install: pip install speech-recognition pyttsx3 gtts pygame")

class VoiceProcessor:
    """
    Voice processing class for speech-to-text and text-to-speech functionality
    Supports multiple languages for accessibility
    """
    
    def __init__(self):
        self.voice_available = VOICE_AVAILABLE
        
        if self.voice_available:
            self._init_speech_recognition()
            self._init_text_to_speech()
            self._init_language_mappings()
        else:
            st.error("Voice processing not available. Please install required libraries.")
    
    def _init_speech_recognition(self):
        """Initialize speech recognition"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
        except Exception as e:
            st.error(f"Failed to initialize speech recognition: {e}")
            self.voice_available = False
    
    def _init_text_to_speech(self):
        """Initialize text-to-speech"""
        try:
            # Initialize pygame for audio playback
            pygame.mixer.init()
            
            # Initialize pyttsx3 for offline TTS
            self.tts_engine = pyttsx3.init()
            
            # Configure TTS settings
            voices = self.tts_engine.getProperty('voices')
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)
            
            self.tts_engine.setProperty('rate', 150)  # Speed of speech
            self.tts_engine.setProperty('volume', 0.8)  # Volume level
            
        except Exception as e:
            st.warning(f"Failed to initialize text-to-speech: {e}")
    
    def _init_language_mappings(self):
        """Initialize language mappings for voice processing"""
        self.language_mappings = {
            "en": {
                "stt": "en-US",
                "tts": "en",
                "gtts": "en"
            },
            "am": {
                "stt": "am-ET", 
                "tts": "am",
                "gtts": "am"
            },
            "om": {
                "stt": "om-ET",
                "tts": "om", 
                "gtts": "om"
            },
            "ti": {
                "stt": "ti-ET",
                "tts": "ti",
                "gtts": "ti"
            },
            "yo": {
                "stt": "yo-NG",
                "tts": "yo",
                "gtts": "yo"
            },
            "sw": {
                "stt": "sw-KE",
                "tts": "sw",
                "gtts": "sw"
            }
        }
    
    def speech_to_text(self, language: str = "en", timeout: int = 5) -> Optional[str]:
        """
        Convert speech to text using microphone input
        
        Args:
            language: Language code for speech recognition
            timeout: Timeout in seconds for listening
            
        Returns:
            Recognized text or None if failed
        """
        if not self.voice_available:
            st.error("Voice processing not available")
            return None
        
        try:
            lang_code = self.language_mappings.get(language, {}).get("stt", "en-US")
            
            with self.microphone as source:
                st.info(f"🎤 Listening... (Language: {language})")
                audio = self.recognizer.listen(source, timeout=timeout)
            
            st.info("🔄 Processing speech...")
            text = self.recognizer.recognize_google(audio, language=lang_code)
            
            return text.strip()
            
        except sr.WaitTimeoutError:
            st.warning("⏰ Listening timeout. Please try again.")
            return None
        except sr.UnknownValueError:
            st.warning("❓ Could not understand audio. Please try again.")
            return None
        except sr.RequestError as e:
            st.error(f"❌ Speech recognition service error: {e}")
            return None
        except Exception as e:
            st.error(f"❌ Speech recognition error: {e}")
            return None
    
    def text_to_speech(self, text: str, language: str = "en", method: str = "gtts") -> bool:
        """
        Convert text to speech
        
        Args:
            text: Text to convert to speech
            language: Language code for TTS
            method: TTS method ('gtts' for Google TTS, 'pyttsx3' for offline)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.voice_available:
            st.error("Voice processing not available")
            return False
        
        if not text.strip():
            st.warning("No text to convert to speech")
            return False
        
        try:
            if method == "gtts":
                return self._gtts_speak(text, language)
            else:
                return self._pyttsx3_speak(text)
                
        except Exception as e:
            st.error(f"Text-to-speech error: {e}")
            return False
    
    def _gtts_speak(self, text: str, language: str) -> bool:
        """Use Google Text-to-Speech for better quality"""
        try:
            lang_code = self.language_mappings.get(language, {}).get("gtts", "en")
            
            # Create TTS object
            tts = gTTS(text=text, lang=lang_code, slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tts.save(tmp_file.name)
                
                # Play audio
                pygame.mixer.music.load(tmp_file.name)
                pygame.mixer.music.play()
                
                # Wait for playback to complete
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                # Clean up
                os.unlink(tmp_file.name)
            
            return True
            
        except Exception as e:
            st.warning(f"Google TTS failed: {e}. Falling back to offline TTS.")
            return self._pyttsx3_speak(text)
    
    def _pyttsx3_speak(self, text: str) -> bool:
        """Use pyttsx3 for offline text-to-speech"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            return True
            
        except Exception as e:
            st.error(f"Offline TTS failed: {e}")
            return False
    
    def get_available_languages(self) -> List[str]:
        """Get list of available languages for voice processing"""
        return list(self.language_mappings.keys())
    
    def get_language_info(self, language: str) -> Dict:
        """Get language information for voice processing"""
        return self.language_mappings.get(language, self.language_mappings["en"])
    
    def is_voice_available(self) -> bool:
        """Check if voice processing is available"""
        return self.voice_available
    
    def test_microphone(self) -> bool:
        """Test microphone functionality"""
        if not self.voice_available:
            return False
        
        try:
            with self.microphone as source:
                st.info("🎤 Testing microphone... Please speak for 2 seconds.")
                audio = self.recognizer.listen(source, timeout=2)
            
            st.success("✅ Microphone test successful!")
            return True
            
        except Exception as e:
            st.error(f"❌ Microphone test failed: {e}")
            return False
    
    def test_speakers(self) -> bool:
        """Test speaker functionality"""
        if not self.voice_available:
            return False
        
        try:
            test_text = "Speaker test successful!"
            return self.text_to_speech(test_text, method="pyttsx3")
            
        except Exception as e:
            st.error(f"❌ Speaker test failed: {e}")
            return False
    
    def get_voice_settings(self) -> Dict:
        """Get current voice settings"""
        if not self.voice_available:
            return {}
        
        try:
            return {
                "rate": self.tts_engine.getProperty('rate'),
                "volume": self.tts_engine.getProperty('volume'),
                "voice": self.tts_engine.getProperty('voice')
            }
        except:
            return {}
    
    def set_voice_settings(self, rate: int = 150, volume: float = 0.8):
        """Set voice settings"""
        if not self.voice_available:
            return
        
        try:
            self.tts_engine.setProperty('rate', rate)
            self.tts_engine.setProperty('volume', volume)
        except Exception as e:
            st.warning(f"Failed to set voice settings: {e}")
    
    def process_voice_command(self, command: str) -> Dict:
        """
        Process voice commands for platform control
        
        Args:
            command: Voice command text
            
        Returns:
            Command result dictionary
        """
        command_lower = command.lower()
        
        # Navigation commands
        if any(word in command_lower for word in ["help", "assistance", "support"]):
            return {
                "type": "help",
                "message": "I'm here to help! You can ask me questions about your studies.",
                "action": "show_help"
            }
        
        elif any(word in command_lower for word in ["progress", "stats", "analytics"]):
            return {
                "type": "progress",
                "message": "Let me show you your learning progress.",
                "action": "show_progress"
            }
        
        elif any(word in command_lower for word in ["language", "change language"]):
            return {
                "type": "language",
                "message": "I can help you change the language. What language would you prefer?",
                "action": "change_language"
            }
        
        elif any(word in command_lower for word in ["level", "difficulty", "beginner", "advanced"]):
            return {
                "type": "level",
                "message": "I can adjust the learning level. What level would you like?",
                "action": "change_level"
            }
        
        else:
            return {
                "type": "question",
                "message": "I understand you have a question. Please ask me anything about your studies.",
                "action": "process_question"
            }
    
    def create_voice_interface(self):
        """Create voice interface controls for Streamlit"""
        if not self.voice_available:
            st.error("Voice processing not available")
            return
        
        st.subheader("🎤 Voice Controls")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎤 Start Voice Input", type="primary"):
                with st.spinner("🎤 Listening..."):
                    voice_text = self.speech_to_text()
                    if voice_text:
                        st.session_state.voice_input = voice_text
                        st.success(f"🎤 Heard: {voice_text}")
        
        with col2:
            if st.button("🔊 Test Speakers"):
                if self.test_speakers():
                    st.success("✅ Speaker test successful!")
                else:
                    st.error("❌ Speaker test failed")
        
        # Voice settings
        with st.expander("🎛️ Voice Settings"):
            rate = st.slider("Speech Rate", 100, 300, 150)
            volume = st.slider("Volume", 0.0, 1.0, 0.8)
            
            if st.button("Apply Settings"):
                self.set_voice_settings(rate, volume)
                st.success("Voice settings updated!")
        
        # Language selection for voice
        voice_language = st.selectbox(
            "Voice Language",
            options=self.get_available_languages(),
            format_func=lambda x: self.get_language_info(x)["stt"]
        )
        
        st.session_state.voice_language = voice_language
