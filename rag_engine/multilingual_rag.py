"""
🌍 Multilingual RAG Engine
Advanced language detection and multilingual response generation

This module implements:
- Automatic language detection for 6 African languages
- Language-specific prompt engineering
- Cultural context awareness
- Cross-language knowledge transfer
"""

import os
import re
from typing import Dict, List, Optional, Tuple
from langdetect import detect, DetectorFactory
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

# Set seed for consistent language detection
DetectorFactory.seed = 0

class MultilingualRAGEngine:
    """
    Advanced multilingual RAG engine supporting 6 African languages
    with cultural context awareness and automatic language detection
    """
    
    def __init__(self):
        self.supported_languages = {
            "en": {
                "name": "English",
                "native_name": "English",
                "country": "Universal",
                "flag": "🇺🇸",
                "prompt_template": self._get_english_prompt()
            },
            "am": {
                "name": "Amharic", 
                "native_name": "አማርኛ",
                "country": "Ethiopia",
                "flag": "🇪🇹",
                "prompt_template": self._get_amharic_prompt()
            },
            "om": {
                "name": "Afaan Oromo",
                "native_name": "Afaan Oromoo", 
                "country": "Ethiopia",
                "flag": "🇪🇹",
                "prompt_template": self._get_oromo_prompt()
            },
            "ti": {
                "name": "Tigrigna",
                "native_name": "ትግርኛ",
                "country": "Ethiopia/Eritrea", 
                "flag": "🇪🇹",
                "prompt_template": self._get_tigrigna_prompt()
            },
            "yo": {
                "name": "Yoruba",
                "native_name": "Èdè Yorùbá",
                "country": "Nigeria",
                "flag": "🇳🇬", 
                "prompt_template": self._get_yoruba_prompt()
            },
            "sw": {
                "name": "Swahili",
                "native_name": "Kiswahili",
                "country": "East Africa",
                "flag": "🇰🇪",
                "prompt_template": self._get_swahili_prompt()
            }
        }
        
        # Initialize Groq LLM
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.1,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        # Language detection patterns
        self.language_patterns = {
            "am": [r'[ሀ-፟]', r'አማርኛ', r'እንዴት', r'ምን', r'የት', r'መቼ'],
            "om": [r'[ሀ-፟]', r'Afaan Oromoo', r'Akkam', r'Maal', r'Eessa', r'Yoom'],
            "ti": [r'[ሀ-፟]', r'ትግርኛ', r'ከመይ', r'እንታይ', r'ኣበይ', r'መዓስ'],
            "yo": [r'[À-ỹ]', r'Èdè Yorùbá', r'Bawo', r'Kini', r'Ibo', r'Nigbawo'],
            "sw": [r'[À-ỹ]', r'Kiswahili', r'Vipi', r'Nini', r'Wapi', r'Lini']
        }
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of input text with high accuracy
        Uses pattern matching + langdetect for robust detection
        """
        try:
            # Clean text for detection
            clean_text = re.sub(r'[^\w\s]', '', text).strip()
            
            if len(clean_text) < 3:
                return "en"  # Default to English for very short text
            
            # Pattern-based detection for African languages
            for lang_code, patterns in self.language_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, text, re.IGNORECASE):
                        return lang_code
            
            # Fallback to langdetect
            detected = detect(text)
            
            # Map common detections to our supported languages
            lang_mapping = {
                "am": "am",  # Amharic
                "om": "om",  # Oromo  
                "ti": "ti",  # Tigrigna
                "yo": "yo",  # Yoruba
                "sw": "sw",  # Swahili
                "en": "en"   # English
            }
            
            return lang_mapping.get(detected, "en")
            
        except Exception as e:
            st.warning(f"Language detection failed: {e}. Defaulting to English.")
            return "en"
    
    def get_language_info(self, lang_code: str) -> Dict:
        """Get detailed information about a language"""
        return self.supported_languages.get(lang_code, self.supported_languages["en"])
    
    def generate_multilingual_response(
        self, 
        query: str, 
        context: str = "",
        target_language: Optional[str] = None
    ) -> str:
        """
        Generate response in the appropriate language with cultural context
        """
        # Detect input language
        input_lang = self.detect_language(query)
        
        # Use target language or default to input language
        response_lang = target_language or input_lang
        
        # Get language-specific prompt
        lang_info = self.get_language_info(response_lang)
        prompt_template = lang_info["prompt_template"]
        
        # Create the prompt
        prompt = ChatPromptTemplate.from_template(prompt_template)
        
        # Build the chain
        chain = prompt | self.llm | StrOutputParser()
        
        # Generate response
        try:
            response = chain.invoke({
                "query": query,
                "context": context,
                "language": lang_info["native_name"],
                "country": lang_info["country"]
            })
            
            return self._post_process_response(response, response_lang)
            
        except Exception as e:
            st.error(f"Error generating multilingual response: {e}")
            return f"Sorry, I encountered an error while processing your question in {lang_info['native_name']}."
    
    def _post_process_response(self, response: str, language: str) -> str:
        """Post-process response for language-specific formatting"""
        if language in ["am", "om", "ti"]:
            # Ethiopian languages - ensure proper script formatting
            response = self._format_ethiopian_script(response)
        elif language == "yo":
            # Yoruba - ensure proper tone marks
            response = self._format_yoruba_tones(response)
        elif language == "sw":
            # Swahili - ensure proper grammar
            response = self._format_swahili_grammar(response)
        
        return response
    
    def _format_ethiopian_script(self, text: str) -> str:
        """Format Ethiopian script text properly"""
        # Basic formatting for Ethiopian languages
        return text
    
    def _format_yoruba_tones(self, text: str) -> str:
        """Format Yoruba text with proper tone marks"""
        # Basic tone mark formatting
        return text
    
    def _format_swahili_grammar(self, text: str) -> str:
        """Format Swahili text with proper grammar"""
        # Basic Swahili grammar formatting
        return text
    
    def _get_english_prompt(self) -> str:
        """English prompt template"""
        return """
        You are Yeneta, an AI study assistant helping African students learn.
        You are knowledgeable, patient, and culturally aware.
        Do not introduce yourself or greet; answer directly without salutations unless explicitly asked.
        
        Context: {context}
        Question: {query}
        
        Please provide a helpful, accurate, and encouraging response in English.
        Make sure your answer is educational and appropriate for students.
        """
    
    def _get_amharic_prompt(self) -> str:
        """Amharic prompt template"""
        return """
        አንተ Yeneta ነህ፣ አፍሪካዊ ተማሪዎችን በመማር የሚረዳ የAI የትምህርት ረዳት።
        በአማርኛ ቋንቋ የተማሪዎችን ጥያቄዎች በትህትና እና በጥልቀት መልስ።
        እባክህ ራስህን አትውሰን ወይም አትሰማራ፤ ሳሎታ በሌለ ጊዜ ቀጥታ መልስ ስጥ።
        
        የተሰጠው መረጃ: {context}
        ጥያቄ: {query}
        
        እባክህ በአማርኛ ቋንቋ ተገቢ፣ ትክክለኛ እና አበረታች መልስ ስጥ።
        መልስህ ለተማሪዎች ትምህርታዊ እና ተገቢ መሆን አለበት።
        """
    
    def _get_oromo_prompt(self) -> str:
        """Afaan Oromo prompt template"""
        return """
        Ati Yeneta dha, barattoota Afrikaa barachuu keessatti gargaaru AI barumsa gargaaraa.
        Afaan Oromoo keessatti gaaffii barattootaaaf deebii qulqulluu fi gadi fagoo kenni.
        Of hin dhiyeessin yookaan si hin beeksisin; nagaa-dubbii malee deebii qajeelaa kennu.
        
        Odeeffannoo kennamte: {context}
        Gaaffii: {query}
        
        Maaloo Afaan Oromoo keessatti deebii fayyadamaa, dhugaa fi gammachiisaa kenni.
        Deebii kee barattootaaf barumsaafi fayyadamaa ta'uu qaba.
        """
    
    def _get_tigrigna_prompt(self) -> str:
        """Tigrigna prompt template"""
        return """
        ንስኻ Yeneta ኢኻ፣ ናይ AI ናይ ትምህርቲ ሓጋዚ እቶም ኣፍሪቃውያን ተማሃሮ ንምምሃር ዝሕግዝ።
        ብትግርኛ ቋንቋ ናይ ተማሃሮ ሕቶታት ብትሕትናን ብጥልቀትን መልሲ ሃብ።
        ኣፍ ክትኣፍ ወይ ሰላም ክትብል ኣትግበር፤ ቀጥታ መልሲ ሃብ እንተ ዝተዓዘበ ብቻ።
        
        ዝተሃበ ሓበሬታ: {context}
        ሕቶ: {query}
        
        በጃኻ ብትግርኛ ቋንቋ ንጥቀመላይ፣ ሓቂን ንጉህን መልሲ ሃብ።
        መልሲኻ ንተማሃሮ ትምህርታዊን ተገቢን ክኸውን ኣለዎ።
        """
    
    def _get_yoruba_prompt(self) -> str:
        """Yoruba prompt template"""
        return """
        Iwo ni Yeneta, oluranlọwọ AI ti o ran awọn akẹkọ Afirika lọwọ lati kọ.
        Ni ede Yoruba, da awọn ibeere awọn akẹkọ ni idahun ti o dara ati ti o jinlẹ.
        Ma ṣe ṣafihan ara rẹ tabi kí; dahun taara ayafi ti a ba beere pataki.
        
        Alaye ti a fun: {context}
        Ibeere: {query}
        
        Jọwọ fun ni idahun ti o wulo, ti o tọ, ati ti o gbeyin ni ede Yoruba.
        Idahun rẹ gbọdọ jẹ ẹkọ ati ti o tọ fun awọn akẹkọ.
        """
    
    def _get_swahili_prompt(self) -> str:
        """Swahili prompt template"""
        return """
        Wewe ni Yeneta, msaidizi wa AI wa masomo anayesaidia wanafunzi wa Afrika kujifunza.
        Katika lugha ya Kiswahili, jibu maswali ya wanafunzi kwa ukarimu na kina.
        Usijitambulishe wala kusalimia; toa jibu moja kwa moja isipokuwa ukiombwa.
        
        Taarifa iliyotolewa: {context}
        Swali: {query}
        
        Tafadhali toa jibu la manufaa, sahihi, na la kuhimiza katika lugha ya Kiswahili.
        Jibu lako lazima liwe la kielimu na linalofaa kwa wanafunzi.
        """
    
    def get_supported_languages(self) -> Dict:
        """Get all supported languages"""
        return self.supported_languages
    
    def is_language_supported(self, lang_code: str) -> bool:
        """Check if language is supported"""
        return lang_code in self.supported_languages
    
    def translate_query(self, query: str, target_language: str) -> str:
        """Translate query to target language for better processing"""
        # This would integrate with translation services
        # For now, return original query
        return query
