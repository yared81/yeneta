import streamlit as st
import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

# Add the project root to Python path and load environment
project_root = Path(__file__).parent
sys.path.append(str(project_root))
# Load environment variables from .env in this folder; if not found, also try parent project root
loaded = load_dotenv(dotenv_path=project_root / ".env", override=True)
if not loaded:
    load_dotenv(dotenv_path=project_root.parent / ".env", override=True)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Import RAG components
try:
    from rag_engine.multilingual_rag import MultilingualRAGEngine
    from rag_engine.adaptive_rag import AdaptiveRAGEngine
    from rag_engine.reflective_rag import SelfReflectiveRAG
    from rag_engine.memory_rag import MemoryAugmentedRAG
    from rag_engine.hybrid_search import HybridSearchEngine
    from features.voice_processing import VoiceProcessor
    from features.progress_tracking import ProgressTracker
    from features.smart_learning_paths import SmartLearningPaths
    from features.advanced_analytics import AdvancedAnalytics
    from features.gamification import GamificationEngine
    RAG_AVAILABLE = True
except ImportError as e:
    st.warning(f"Some RAG components not available: {e}")
    RAG_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title=" Yeneta - Multilingual AI Study Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit default elements and add custom styling
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > div[data-testid="stToolbar"] {visibility: hidden;}
    .stApp > div[data-testid="stDecoration"] {visibility: hidden;}
    .stApp > div[data-testid="stStatusWidget"] {visibility: hidden;}
    .stApp > div[data-testid="stHeader"] {visibility: hidden;}
    
    /* Global Styles */
    .main .block-container {
        padding: 0;
        max-width: 100%;
    }
    
    .stApp {
        background: #f8f9fa;
    }
    
    /* Fix text visibility */
    .stMarkdown {
        color: #2c3e50 !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #2c3e50 !important;
    }
    
    .stMarkdown p {
        color: #495057 !important;
    }
    
    .stMarkdown strong {
        color: #2c3e50 !important;
    }
    
    .stMarkdown em {
        color: #6c757d !important;
    }
    
    /* Navigation Bar */
    .navbar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 0;
        position: fixed;
        top: 0;
        width: 100%;
        z-index: 1000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .nav-container {
        max-width: 100%;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 1rem;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .nav-left { display: flex; align-items: center; gap: 1.5rem; }
    
    .nav-logo {
        font-size: 1.8rem;
        font-weight: 800;
        color: white;
        text-decoration: none;
    }
    
    .nav-links { display: flex; gap: 1.25rem; align-items: center; white-space: nowrap; }
    
    .nav-link {
        color: white;
        text-decoration: none !important;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    
    .nav-link:hover {
        background: rgba(255,255,255,0.2);
        color: white;
        text-decoration: none !important;
    }
    
    .nav-buttons { display: flex; gap: 0.5rem; white-space: nowrap; }
    
    .btn-primary {
        background: white;
        color: #667eea;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        text-decoration: none !important;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        color: #667eea;
        text-decoration: none !important;
    }
    
    .btn-secondary {
        background: transparent;
        color: white;
        padding: 0.5rem 1.5rem;
        border: 2px solid white;
        border-radius: 25px;
        text-decoration: none !important;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .btn-secondary:hover {
        background: white;
        color: #667eea;
        transform: translateY(-2px);
        text-decoration: none !important;
    }
    
    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 0 2rem 0;
        text-align: center;
        color: white;
        margin-top: 60px;
    }
    
    .hero-content {
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 1rem !important;
        text-align: left !important;
    }
    
    .hero h1 {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .hero h2 {
        font-size: 1.5rem;
        font-weight: 400;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    
    .hero p {
        font-size: 1.2rem;
        margin-bottom: 3rem;
        opacity: 0.8;
        line-height: 1.6;
    }
    
    .hero-quote {
        font-size: 1.1rem;
        font-style: italic;
        margin: 2rem 0;
        opacity: 0.9;
        border-left: 4px solid white;
        padding-left: 2rem;
    }
    
    .hero-buttons {
        display: flex;
        gap: 1rem;
        justify-content: center;
        flex-wrap: wrap;
    }
    
    .btn-hero {
        background: #ffffff !important;
        color: #333333 !important;
        padding: 1rem 2rem;
        border-radius: 30px;
        text-decoration: none !important;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        display: inline-block;
    }
    
    .btn-hero:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        color: #667eea;
        text-decoration: none !important;
    }
    
    .btn-hero-outline {
        background: transparent !important;
        color: #ffffff !important;
        padding: 1rem 2rem;
        border: 2px solid white;
        border-radius: 30px;
        text-decoration: none !important;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        cursor: pointer;
        display: inline-block;
    }
    
    .btn-hero-outline:hover {
        background: white;
        color: #667eea;
        transform: translateY(-3px);
        text-decoration: none !important;
    }
    
    /* Section Styles */
    .section {
        padding: 4rem 0;
        background: white;
    }
    
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
        color: #2c3e50;
    }
    
    .section-subtitle {
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 3rem;
        color: #6c757d;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* About Section */
    .about-content {
        text-align: left !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 1rem !important;
    }
    
    .about-description {
        font-size: 1.2rem;
        line-height: 1.8;
        color: #495057;
        margin-bottom: 3rem;
    }
    
    .about-stats {
        display: flex;
        justify-content: center;
        gap: 3rem;
        flex-wrap: wrap;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-item h3 {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .stat-item p {
        font-size: 1.1rem;
        color: #6c757d;
        margin: 0;
    }
    
    /* Features Section */
    .features-section {
        background: #f8f9fa;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
        margin-top: 3rem;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid #e9ecef;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
    }
    
    .feature-card h3 {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #2c3e50;
    }
    
    .feature-card p {
        color: #6c757d;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Contact Section */
    .contact-section {
        background: #f8f9fa;
    }
    
    .contact-content {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 4rem;
        margin-top: 3rem;
    }
    
    .contact-info h3,
    .contact-message h3 {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 2rem;
        color: #2c3e50;
    }
    
    .contact-item {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    
    .contact-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
        color: #667eea;
    }
    
    .contact-text {
        color: #495057;
        font-size: 1.1rem;
    }
    
    .contact-message p {
        color: #6c757d;
        line-height: 1.6;
        margin-bottom: 2rem;
    }
    
    .quote-box {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    
    .quote-box p {
        font-style: italic;
        color: #495057;
        margin-bottom: 1rem;
    }
    
    .quote-box strong {
        color: #667eea;
    }
    
    .section-dark {
        background: #f8f9fa;
    }
    
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
        color: #2c3e50;
    }
    
    .section-subtitle {
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 3rem;
        color: #7f8c8d;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Feature Grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid #e9ecef;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #2c3e50;
    }
    
    .feature-description {
        color: #6c757d;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    /* About Section */
    .about-content {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 3rem;
        align-items: center;
        margin: 3rem 0;
    }
    
    .about-text {
        font-size: 1.1rem;
        line-height: 1.8;
        color: #495057;
    }
    
    .about-stats {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 2rem;
    }
    
    .stat-item {
        text-align: center;
        padding: 1.5rem;
        background: #f8f9fa;
        border-radius: 10px;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #6c757d;
        font-weight: 500;
    }
    
    /* Contact Section */
    .contact-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 3rem;
        margin: 3rem 0;
    }
    
    .contact-info {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
    }
    
    .contact-item {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    
    .contact-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
        color: #667eea;
    }
    
    .contact-text {
        color: #495057;
        font-size: 1.1rem;
    }
    
    /* Footer */
    .footer {
        background: #111111 !important; /* ensure dark background */
        color: #ffffff !important;      /* ensure light text */
        padding: 0 !important;
        text-align: left !important;
        width: 100vw !important;
        margin: 0 !important;
    }
    /* Ensure footer text remains readable on dark background */
    .footer, .footer *, .footer a, .footer a:visited {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important; /* Safari/Chrome */
        text-shadow: none !important;
        opacity: 1 !important;
    }
    .footer a:hover { color: #a8b3ff !important; }
    
    .footer-content {
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0.25rem 0.75rem !important;
    }
    
    .footer-title {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 1rem;
    }
    
    .footer-description {
        font-size: 1.1rem;
        opacity: 0.8;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    .footer-links {
        display: flex;
        justify-content: flex-start !important;
        gap: 1rem !important;
        margin: 0.25rem 0.75rem !important;
        flex-wrap: wrap;
    }
    .footer-link { color: #ecf0f1 !important; }
    .footer-link:hover { color: #667eea !important; }
    
    .footer-link {
        color: white;
        text-decoration: none !important;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .footer-link:hover {
        color: #667eea;
        text-decoration: none !important;
    }
    
    .footer-bottom {
        border-top: 1px solid #34495e;
        padding-top: 0.75rem;
        margin-top: 0.75rem;
        opacity: 0.7;
    }
    
    /* Dashboard Styles */
    .dashboard-header {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .dashboard-subtitle {
        color: #6c757d;
        font-size: 1.2rem;
    }
    
    /* Chat Interface */
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    .chat-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f8f9fa;
    }
    
    .chat-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2c3e50;
    }
    
    .upload-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .upload-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    /* Button Styles */
    .stButton > button {
        background: #ffffff !important;
        color: #333333 !important;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        font-size: 1rem;
        width: 100%;
    }
    /* Text fields and chat input colors (force light background + dark text) */
    input, textarea, select { background: #ffffff !important; color: #111111 !important; caret-color: #111111 !important; }
    input[type="text"], input[type="search"], input[type="number"], input[type="email"], input[type="password"],
    textarea { background: #ffffff !important; color: #111111 !important; border: 1px solid #ced4da !important; }
    .stTextInput input, .stTextArea textarea { background: #ffffff !important; color: #111111 !important; border: 1px solid #ced4da !important; }
    .stSelectbox [data-baseweb="select"] > div, .stMultiSelect [data-baseweb="select"] > div { background: #ffffff !important; color: #111111 !important; border: 1px solid #ced4da !important; }
    .stSelectbox [role="combobox"], .stMultiSelect [role="combobox"] { background: #ffffff !important; color: #111111 !important; }
    [data-baseweb="input"] input, [data-baseweb="textarea"] textarea { background: #ffffff !important; color: #111111 !important; }
    ::placeholder { color: #6c757d !important; opacity: 1 !important; }
    :-ms-input-placeholder { color: #6c757d !important; }
    ::-ms-input-placeholder { color: #6c757d !important; }
    label, .stMarkdown label, .stSelectbox label, .stMultiSelect label { color: #2c3e50 !important; }

    /* Chat input colors */
    [data-testid="stChatInput"] textarea { background: #ffffff !important; color: #333333 !important; }
    [data-testid="stChatInput"] button { background: #ffffff !important; color: #333333 !important; border: 1px solid #ced4da !important; }
    .upload-section { background: #ffffff !important; color: #333333 !important; }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero h1 {
            font-size: 2.5rem;
        }
        
        .hero-buttons {
            flex-direction: column;
            align-items: center;
        }
        
        .about-content {
            grid-template-columns: 1fr;
        }
        
        .contact-grid {
            grid-template-columns: 1fr;
        }
        
        .nav-links {
            display: none;
        }
    }

    /* Spacing overrides to ensure tighter layout */
    .hero { padding: 2rem 0 1rem 0 !important; margin-top: 40px !important; }
    .footer { padding: 0.75rem 0 !important; }
    .footer-content { max-width: 100% !important; padding: 0 0.5rem !important; }
    .footer-links { gap: 1rem !important; }
    .section { padding: 2.5rem 0 !important; }
    /* Make anchors scroll nicely below fixed navbar */
    html { scroll-behavior: smooth; }
    .section, .hero { scroll-margin-top: 90px; }

    /* Ensure text is readable (fix cases where text only shows on selection) */
    html, body, .stApp {
        color: #111111 !important;
        background: #ffffff !important;
    }
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span, .stMarkdown div,
    p, li, span, div {
        color: #111111 !important;
    }
    /* Do not override footer contrast */
    .footer, .footer * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        opacity: 1 !important;
    }
    h1, h2, h3, h4, h5, h6 { color: #2c3e50 !important; }
    a { color: #2c3e50 !important; text-decoration: none !important; }
    a:hover { color: #667eea !important; text-decoration: none !important; }
    ::selection { background: #cfe2ff; color: #2c3e50; }

    /* Full-width layout and zero left padding */
    html, body { margin: 0 !important; padding: 0 !important; }
    .stApp { margin: 0 !important; padding: 0 !important; }
    [data-testid="stAppViewContainer"] { padding: 0 !important; }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="block-container"], .main .block-container { margin: 0 !important; padding-left: 0 !important; padding-right: 0 !important; max-width: 100% !important; }
    .container { max-width: 100% !important; padding-left: 0 !important; padding-right: 0 !important; margin: 0 !important; }
    .nav-container { max-width: 100% !important; padding-left: 0 !important; padding-right: 0 !important; margin: 0 !important; }
    :root { --st-edge-padding: 0px !important; }

    /* Hard overrides to eliminate left offset and avoid wrapping */
    *, *::before, *::after { box-sizing: border-box !important; }
    .navbar { left: 0; right: 0; width: 100vw; box-sizing: border-box; }
    .nav-container { width: 100% !important; overflow-x: auto; white-space: nowrap; }
    .nav-left { flex-wrap: nowrap; }
    .nav-links { flex-wrap: nowrap; }
    .nav-buttons { flex-wrap: nowrap; }
    .nav-logo { display: inline-block; }
    .nav-link, .btn-primary, .btn-secondary { display: inline-block; }
    .nav-links { gap: 0.9rem !important; }
    .nav-buttons { gap: 0.5rem !important; }

    /* Prevent nav wrapping and compress spacing */
    .nav-links { gap: 1rem !important; }
    .nav-buttons { gap: 0.5rem !important; }
    .btn-primary, .btn-secondary { padding: 0.4rem 1rem !important; }

    @media (max-width: 992px) {
        .nav-links { display: none !important; }
        .nav-buttons { gap: 0.5rem !important; }
        .btn-primary, .btn-secondary { padding: 0.4rem 0.8rem !important; }
    }
</style>
""", unsafe_allow_html=True)

class YenetaApp:
    def __init__(self):
        self.initialize_session_state()
        if RAG_AVAILABLE:
            self.setup_rag_engines()
    
    def _extract_text_from_bytes(self, data: bytes, filename: str) -> str:
        """Best-effort text extraction from common doc types for local context building."""
        name_lower = filename.lower()
        # PDF
        if name_lower.endswith('.pdf'):
            try:
                from io import BytesIO
                from pypdf import PdfReader
                reader = PdfReader(BytesIO(data))
                texts = []
                for page in reader.pages[:10]:
                    texts.append(page.extract_text() or "")
                return "\n".join(texts)
            except Exception:
                return ""
        # DOCX
        if name_lower.endswith('.docx'):
            try:
                from io import BytesIO
                import docx
                doc = docx.Document(BytesIO(data))
                return "\n".join(p.text for p in doc.paragraphs)
            except Exception:
                return ""
        # Markdown / Text
        try:
            return data.decode('utf-8', errors='ignore')
        except Exception:
            return ""
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False
        if "user" not in st.session_state:
            st.session_state.user = None
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Home"
        if "show_public" not in st.session_state:
            st.session_state.show_public = False
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "message_subjects" not in st.session_state:
            st.session_state.message_subjects = {}
        if "rag_engines_initialized" not in st.session_state:
            st.session_state.rag_engines_initialized = False
        if "uploaded_files" not in st.session_state:
            st.session_state.uploaded_files = []
        if "file_summaries" not in st.session_state:
            st.session_state.file_summaries = {}
        if "study_plans" not in st.session_state:
            st.session_state.study_plans = {}
        if "quizzes" not in st.session_state:
            st.session_state.quizzes = {}
        if "user_profile" not in st.session_state:
            st.session_state.user_profile = {
                "name": "Student",
                "email": "student@yeneta.com",
                "language_preference": "English",
                "learning_level": "Beginner"
            }
    
    def setup_rag_engines(self):
        """Initialize all RAG engines"""
        if not st.session_state.get('rag_engines_initialized', False):
            try:
                if not GROQ_API_KEY:
                    st.warning("⚠️ GROQ_API_KEY not found. AI responses may be limited.")
                
                self.multilingual_rag = MultilingualRAGEngine()
                self.adaptive_rag = AdaptiveRAGEngine()
                self.self_reflective_rag = SelfReflectiveRAG()
                self.memory_rag = MemoryAugmentedRAG()
                self.hybrid_search = HybridSearchEngine()
                
                self.voice_processor = VoiceProcessor()
                self.progress_tracker = ProgressTracker()
                self.smart_learning_paths = SmartLearningPaths()
                self.advanced_analytics = AdvancedAnalytics()
                self.gamification_engine = GamificationEngine()
                
                st.session_state.rag_engines_initialized = True
                
            except Exception as e:
                st.error(f"❌ Error initializing RAG engines: {e}")
                st.session_state.rag_engines_initialized = False

    def render_navigation(self):
        """Render the main navigation bar"""
        # Visual header bar with inline nav next to logo
        st.markdown("""
        <nav class="navbar">
            <div class="nav-container">
                <div class="nav-left">
                    <span class="nav-logo">Yeneta</span>
                <div class="nav-links">
                        <a href="#hero" class="nav-link">Home</a>
                        <a href="#about" class="nav-link">About Us</a>
                        <a href="#features" class="nav-link">Features</a>
                        <a href="#contact" class="nav-link">Contact</a>
                    </div>
                </div>
                <div class="nav-buttons">
                    <a href="#hero" class="btn-primary" data-route="Login">Login</a>
                    <a href="#hero" class="btn-secondary" data-route="Sign Up">Sign Up</a>
                </div>
            </div>
        </nav>
        """, unsafe_allow_html=True)
        
        # In-page smooth scroll for header/footer anchors without reload
        st.markdown(
            """
<script>
document.addEventListener('click', function(e){
  const a = e.target.closest('a');
  if (!a) return;
  const href = a.getAttribute('href') || '';
  if (href.startsWith('#')) {
    e.preventDefault();
    const target = document.querySelector(href);
    if (target) { target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  }
});
</script>
            """,
            unsafe_allow_html=True,
        )
        
        # Smooth in-page scroll for header/footer links
        st.markdown(
            """
<script>
document.addEventListener('click', function(e){
  const a = e.target.closest('a');
  if(!a) return;
  const href = a.getAttribute('href') || '';
  if(href.startsWith('#')){
    e.preventDefault();
    const el = document.querySelector(href);
    if(el){ el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  }
});
</script>
            """,
            unsafe_allow_html=True,
        )

    def render_hero_section(self):
        """Render the hero section with Nelson Mandela quote"""
        st.markdown(
            """
<div id="hero" class="hero">
            <div class="hero-content">
                <h1>🌍 Yeneta</h1>
                <h2>Multilingual AI Study Platform</h2>
<p>Bridging educational gaps across Africa through advanced RAG technology. Supporting 6 African languages with personalized, voice-enabled learning experiences.</p>
<div class="hero-quote">"Education is the most powerful weapon which you can use to change the world."<br><strong>- Nelson Mandela</strong></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Hero buttons using Streamlit
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="hero-buttons">', unsafe_allow_html=True)
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🚀 Join Now", key="hero_join_btn", help="Create your account", use_container_width=True):
                    st.session_state.current_page = "Sign Up"
                    st.rerun()
            with col_btn2:
                if st.button("🔑 Login", key="hero_login_btn", help="Sign in to your account", use_container_width=True):
                    st.session_state.current_page = "Login"
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    def render_about_section(self):
        """Render the about us section"""
        st.markdown(
            """
<section id="about" class="section">
            <div class="container">
                <h2 class="section-title">About Us</h2>
                <div class="about-content">
<p class="about-description">Yeneta is a revolutionary multilingual AI study platform designed specifically for African students. We believe that language should never be a barrier to quality education.<br><br>Our platform leverages advanced RAG (Retrieval-Augmented Generation) technology to provide personalized learning experiences in 6 African languages: Amharic, Afaan Oromo, Tigrigna, English, Yoruba, and Swahili.<br><br>We're committed to making education accessible, engaging, and effective for students across the African continent, regardless of their language or learning level</p>
                    <div class="about-stats">
<div class="stat-item"><h3>6+</h3><p>African Languages</p></div>
<div class="stat-item"><h3>1000+</h3><p>Students Helped</p></div>
<div class="stat-item"><h3>24/7</h3><p>AI Support</p></div>
                        </div>
                        </div>
                        </div>
</section>
            """,
            unsafe_allow_html=True,
        )
        
        # Removed duplicated metrics to avoid repetition under About section

    def render_features_section(self):
        """Render the features section"""
        st.markdown("""
        <section id="features" class="section features-section">
            <div class="container">
                <h2 class="section-title">🌟 Key Features</h2>
                <p class="section-subtitle">Discover the powerful features that make Yeneta the ultimate learning platform</p>
                <div class="features-grid">
                    <article class="feature-card">
                        <div class="feature-icon">🌍</div>
                        <h3>Multilingual Support</h3>
                        <p>Native support for 6 African languages with cultural context awareness.</p>
                    </article>
                    <article class="feature-card">
                        <div class="feature-icon">🧠</div>
                        <h3>Advanced RAG Technology</h3>
                        <p>Cutting-edge retrieval with adaptive, self-reflective validation.</p>
                    </article>
                    <article class="feature-card">
                        <div class="feature-icon">🎯</div>
                        <h3>Adaptive Learning</h3>
                        <p>Adjusts explanations to your level based on your progress.</p>
                    </article>
                    <article class="feature-card">
                        <div class="feature-icon">🎤</div>
                        <h3>Voice Integration</h3>
                        <p>Speech-to-text and text-to-speech for inclusive learning.</p>
                    </article>
                    <article class="feature-card">
                        <div class="feature-icon">📊</div>
                        <h3>Progress Tracking</h3>
                        <p>Real-time analytics and personalized learning paths.</p>
                    </article>
                    <article class="feature-card">
                        <div class="feature-icon">🔍</div>
                        <h3>Self-Validation</h3>
                        <p>Ensures educational accuracy and appropriateness.</p>
                    </article>
                    </div>
                </div>
        </section>
        """, unsafe_allow_html=True)

    def render_contact_section(self):
        """Render the contact section"""
        st.markdown("""
        <section id="contact" class="section contact-section">
            <div class="container">
                <h2 class="section-title">Contact Us</h2>
                <p class="section-subtitle">Get in touch with our team</p>
                <div class="contact-content">
                    <div class="contact-info">
                        <h3>Get in Touch</h3>
                        <div class="contact-item"><span class="contact-icon">📧</span><span class="contact-text">info@yeneta.com</span></div>
                        <div class="contact-item"><span class="contact-icon">📱</span><span class="contact-text">+251 911 234 567</span></div>
                        <div class="contact-item"><span class="contact-icon">📍</span><span class="contact-text">Addis Ababa, Ethiopia</span></div>
                        <div class="contact-item"><span class="contact-icon">🌐</span><span class="contact-text">www.yeneta.com</span></div>
                        </div>
                    <div class="contact-message">
                        <h3>Send us a Message</h3>
                        <p>Have questions about our platform? Want to collaborate? We'd love to hear from you!</p>
                        <div class="quote-box">
                            <p>"The future of education in Africa starts with platforms like Yeneta. We're building bridges between languages, cultures, and knowledge."</p>
                            <strong>- The Yeneta Team</strong>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        """, unsafe_allow_html=True)

    def render_footer(self):
        """Render the footer"""
        st.markdown("""
        <div class="footer">
            <div class="footer-content">
                <div class="footer-title">🌟 Yeneta - Empowering African Students Through AI</div>
                <div class="footer-description">Accessible, personalized, and culturally relevant learning for everyone.</div>
                <div class="footer-links">
                    <a href="#hero" class="footer-link">Home</a>
                    <a href="#about" class="footer-link">About Us</a>
                    <a href="#features" class="footer-link">Features</a>
                    <a href="#contact" class="footer-link">Contact</a>
                </div>
                <div class="footer-bottom">© 2024 Yeneta. All rights reserved. | Privacy Policy | Terms of Service</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    def render_auth_section(self):
        """Render authentication section"""
        st.markdown("### Welcome to Yeneta")
        
        # Authentication tabs
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        with tab1:
            st.markdown("#### Login to Your Account")
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="Enter your email")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                login_button = st.form_submit_button("Login", use_container_width=True)
                
                if login_button:
                    if self.authenticate_user(email, password):
                        st.success("✅ Login successful!")
                        st.session_state.authenticated = True
                        st.session_state.user = {"email": email, "name": email.split("@")[0]}
                        st.session_state.user_profile['name'] = email.split("@")[0]
                        st.session_state.user_profile['email'] = email
                        st.session_state.current_page = "Dashboard"
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Please try again.")
        
        with tab2:
            st.markdown("#### Create New Account")
            with st.form("signup_form"):
                name = st.text_input("Full Name", placeholder="Enter your full name")
                email = st.text_input("Email", placeholder="Enter your email")
                password = st.text_input("Password", type="password", placeholder="Create a password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                signup_button = st.form_submit_button("Sign Up", use_container_width=True)
                
                if signup_button:
                    if password == confirm_password:
                        if self.create_user(name, email, password):
                            st.success("✅ Account created successfully! Please login.")
                        else:
                            st.error("❌ Error creating account. Please try again.")
                    else:
                        st.error("❌ Passwords do not match.")

    def render_dashboard(self):
        """Render the student dashboard with tabs"""
        # Header with home button to return to the main website
        top_col1, top_col2 = st.columns([1, 5])
        with top_col1:
            if st.button("🏠 Home", key="dashboard_home_btn"):
                st.session_state.show_public = True
                st.session_state.current_page = "Home"
                st.rerun()
        with top_col2:
            st.markdown("### 📊 Student Dashboard")
        st.markdown(f"Welcome back, {st.session_state.user_profile['name']}! Here's your learning overview")
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Questions Asked", len([m for m in st.session_state.messages if m["role"] == "user"]))
        with col2:
            st.metric("Files Uploaded", len(st.session_state.uploaded_files))
        with col3:
            st.metric("Learning Level", st.session_state.user_profile['learning_level'])
        with col4:
            st.metric("Language", st.session_state.user_profile['language_preference'])
        
        # Tab navigation
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["💬 Chat", "🕒 History", "📚 Study Plan", "📁 Files", "🧪 Quizzes", "👤 Profile/Progress"])
        
        with tab1:
            self.render_chat_tab()
        with tab2:
            self.render_history_tab()
        with tab3:
            self.render_study_plan_tab()
        with tab4:
            self.render_files_tab()
        with tab5:
            self.render_quizzes_tab()
        with tab6:
            # Combine profile and progress to avoid adding more tabs
            self.render_profile_tab()
            st.markdown("---")
            self.render_progress_tab()

    def render_history_tab(self):
        st.markdown("#### 🕒 Session History")
        # Filters
        fcol1, fcol2 = st.columns([2, 1])
        with fcol1:
            query = st.text_input("Search questions/answers")
        with fcol2:
            subject = st.text_input("Subject tag (optional)")
        # Filter
        items = list(st.session_state.messages)
        if query:
            items = [m for m in items if query.lower() in m.get("content", "").lower()]
        if subject:
            items = [m for m in items if m.get("subject") == subject]
        # Show last N grouped user+assistant pairs
        st.markdown("##### Recent interactions")
        # Build pairs
        pairs = []
        current = {}
        for m in items:
            if m.get("role") == "user":
                current = {"q": m}
            elif m.get("role") == "assistant" and current:
                current["a"] = m
                pairs.append(current)
                current = {}
        for idx, pair in enumerate(reversed(pairs[-20:])):
            q = pair.get("q", {})
            a = pair.get("a", {})
            with st.expander(f"Q: {q.get('content','')[:60]}..."):
                st.write("Question:", q.get("content", ""))
                if a:
                    st.write("Answer:", a.get("content", ""))
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Revisit", key=f"rev_{idx}"):
                        st.session_state.current_page = "Dashboard"
                        st.session_state.show_public = False
                        st.session_state.messages.append({"role": "user", "content": q.get("content", "")})
                        st.rerun()
                with c2:
                    if st.button("Improve answer", key=f"imp_{idx}"):
                        improve_prompt = f"Improve this answer for clarity and completeness, keep it concise. Answer: {a.get('content','')} Context: {q.get('content','')}"
                        st.session_state.messages.append({"role": "user", "content": improve_prompt})
                        st.rerun()

    def _ensure_multilingual(self):
        if not hasattr(self, 'multilingual_rag'):
            try:
                from rag_engine.multilingual_rag import MultilingualRAGEngine
                self.multilingual_rag = MultilingualRAGEngine()
            except Exception as e:
                st.warning(f"RAG engine not available: {e}")

    def render_study_plan_tab(self):
        st.markdown("#### 📚 Study Plan")
        subj = st.text_input("Subject", placeholder="e.g., Mathematics")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Generate/Regenerate Plan") and subj:
                modules = self._generate_study_modules(subj)
                st.session_state.study_plans[subj] = {"modules": modules}
                st.success("Study plan generated.")
        with c2:
            if subj and subj in st.session_state.study_plans and st.button("Clear Plan"):
                st.session_state.study_plans.pop(subj, None)
                st.rerun()
        # Display
        if subj and subj in st.session_state.study_plans:
            modules = st.session_state.study_plans[subj]["modules"]
            for i, m in enumerate(modules):
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    st.write(f"{m['title']} — {m['difficulty']}")
                with col2:
                    new_status = st.selectbox("Status", ["todo","in_progress","done"], index=["todo","in_progress","done"].index(m["status"]), key=f"sp_s_{i}")
                    m["status"] = new_status
                with col3:
                    if st.button("Easier", key=f"sp_e_{i}"):
                        m["difficulty"] = "easy"
                with col4:
                    if st.button("Harder", key=f"sp_h_{i}"):
                        m["difficulty"] = "hard"

    def _generate_study_modules(self, subject: str):
        # Simple heuristic: derive modules from recent questions
        recent_qs = [m["content"] for m in st.session_state.messages if m["role"] == "user"][-5:]
        base = [
            {"title": f"Core concepts in {subject}", "status": "todo", "difficulty": "medium"},
            {"title": f"Key terms and definitions in {subject}", "status": "todo", "difficulty": "easy"},
        ]
        for q in recent_qs:
            base.append({"title": f"Practice: {q[:40]}...", "status": "todo", "difficulty": "medium"})
        return base[:8]

    def render_files_tab(self):
        st.markdown("#### 📁 Files Intelligence")
        if not st.session_state.uploaded_files:
            st.info("Upload files in the Chat tab to see summaries here.")
            return
        for f in st.session_state.uploaded_files:
            name = f.get("name","unknown")
            summary_obj = st.session_state.file_summaries.get(name)
            colA, colB = st.columns([3,1])
            with colA:
                st.markdown(f"**{name}**")
            with colB:
                if st.button("Refresh summary", key=f"refresh_{name}"):
                    st.session_state.file_summaries.pop(name, None)
                    st.rerun()
            if not summary_obj:
                with st.spinner("Summarizing..."):
                    text = self._extract_text_from_bytes(f.get("content", b""), name) if isinstance(f.get("content"), bytes) else (f.get("content") or "")
                    self._ensure_multilingual()
                    if text:
                        prompt = "Summarize this content concisely, list 5 bullet key points, and suggest 5 quiz questions.\n\n" + text[:4000]
                        try:
                            result = self.multilingual_rag.generate_multilingual_response(query=prompt, context="", target_language="en")
                        except Exception as e:
                            result = f"Summary unavailable: {e}"
                    else:
                        result = "No extractable text."
                    st.session_state.file_summaries[name] = {"raw": result}
                    summary_obj = st.session_state.file_summaries[name]
            with st.expander("Summary / Key Points / Suggested Quiz"):
                st.write(summary_obj.get("raw",""))
            if st.button("Ask about this file", key=f"ask_{name}"):
                st.session_state.current_page = "Dashboard"
                st.session_state.show_public = False
                st.session_state.messages.append({"role": "user", "content": f"Based on {name}, explain the main ideas and give examples."})
                st.rerun()

    def render_quizzes_tab(self):
        st.markdown("#### 🧪 Quizzes")
        subj = st.text_input("Subject for quiz", key="quiz_subject")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Generate quiz (5)") and subj:
                questions = self._generate_quiz(subj, 5)
                st.session_state.quizzes[subj] = {"questions": questions, "answers": [None]*len(questions)}
                st.success("Quiz generated.")
        with c2:
            if subj and subj in st.session_state.quizzes and st.button("Clear quiz"):
                st.session_state.quizzes.pop(subj, None)
                st.rerun()
        if subj and subj in st.session_state.quizzes:
            data = st.session_state.quizzes[subj]
            for i, q in enumerate(data["questions"]):
                st.markdown(f"**Q{i+1}.** {q['q']}")
                ans = st.text_input("Your answer", key=f"qa_{i}")
                if st.button("Check", key=f"qc_{i}"):
                    correct = q.get("a","")
                    st.info(f"Correct answer: {correct}")
                    st.write(q.get("explain",""))

    def _generate_quiz(self, subject: str, n: int):
        self._ensure_multilingual()
        try:
            prompt = f"Create {n} short quiz questions about {subject}. For each, provide: Question, Correct answer, and a 1-sentence explanation."
            result = self.multilingual_rag.generate_multilingual_response(query=prompt, context="", target_language="en")
        except Exception as e:
            result = f"Quiz generation unavailable: {e}"
        # Very light parser: split lines
        questions = []
        for line in result.splitlines():
            if not line.strip():
                continue
            if ':' in line:
                # naive parse: "Q: ... A: ..."
                parts = line.split('A:')
                if len(parts) == 2:
                    qtext = parts[0].replace('Q','').replace(':','').strip()
                    atext = parts[1].strip()
                    questions.append({"q": qtext, "a": atext, "explain": ""})
        if not questions:
            # fallback single item
            questions = [{"q": f"What is a key concept in {subject}?", "a": "Definition and example.", "explain": "Concept overview."} for _ in range(n)]
        return questions[:n]

    def render_chat_tab(self):
        """Render the chat tab with file upload and AI chat"""
        st.markdown("#### 💬 AI Study Assistant")
        st.markdown("Upload your study materials and ask questions to get personalized AI responses")
        
        # File upload section
        st.markdown("##### 📁 Upload Study Materials")
        uploaded_files = st.file_uploader(
            "Choose files to upload",
            accept_multiple_files=True,
            type=['pdf', 'txt', 'docx', 'md'],
            help="Upload your study materials to get better AI responses"
        )
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_info = {
                    "name": uploaded_file.name,
                    "size": uploaded_file.size,
                    "type": uploaded_file.type,
                    "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "content": uploaded_file.read()
                }
                
                if not any(f["name"] == file_info["name"] for f in st.session_state.uploaded_files):
                    st.session_state.uploaded_files.append(file_info)
                    st.success(f"✅ Uploaded: {uploaded_file.name}")
        
        # Show uploaded files
        if st.session_state.uploaded_files:
            st.markdown("##### 📚 Your Uploaded Files")
            for i, file_info in enumerate(st.session_state.uploaded_files):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"📄 {file_info['name']}")
                with col2:
                    st.write(f"{file_info['size']} bytes")
                with col3:
                    if st.button("🗑️", key=f"delete_file_{i}", help="Delete file"):
                        st.session_state.uploaded_files.pop(i)
                        st.rerun()
        
        st.markdown("---")
        
        # Use profile settings instead of duplicate selectors
        language = st.session_state.user_profile.get('language_preference', 'English')
        level = st.session_state.user_profile.get('learning_level', 'Beginner')
        
        # Chat messages
        st.markdown("##### 💬 Chat with AI")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about your studies..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = self.generate_ai_response(prompt, language, level)
                    st.markdown(response)
            
            # Add AI response
            st.session_state.messages.append({"role": "assistant", "content": response})

    def render_profile_tab(self):
        """Render the profile tab for editing user settings"""
        st.markdown("#### 👤 Profile Settings")
        st.markdown("Manage your account settings and preferences")
        
        # Profile form
        with st.form("profile_form"):
            st.markdown("##### Personal Information")
            name = st.text_input("Full Name", value=st.session_state.user_profile['name'])
            email = st.text_input("Email", value=st.session_state.user_profile['email'])
            
            st.markdown("##### Learning Preferences")
            language_preference = st.selectbox(
                "Preferred Language",
                ["English", "Amharic", "Afaan Oromo", "Tigrigna", "Yoruba", "Swahili"],
                index=["English", "Amharic", "Afaan Oromo", "Tigrigna", "Yoruba", "Swahili"].index(st.session_state.user_profile['language_preference'])
            )
            
            learning_level = st.selectbox(
                "Learning Level",
                ["Beginner", "Intermediate", "Advanced"],
                index=["Beginner", "Intermediate", "Advanced"].index(st.session_state.user_profile['learning_level'])
            )
            
            if st.form_submit_button("💾 Save Changes", use_container_width=True):
                st.session_state.user_profile.update({
                    "name": name,
                    "email": email,
                    "language_preference": language_preference,
                    "learning_level": learning_level
                })
                st.success("✅ Profile updated successfully!")
                st.rerun()
        
        # Account statistics
        st.markdown("##### 📊 Account Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Questions", len([m for m in st.session_state.messages if m["role"] == "user"]))
        with col2:
            st.metric("Files Uploaded", len(st.session_state.uploaded_files))
        with col3:
            st.metric("Account Created", "Today")

    def render_progress_tab(self):
        """Render the progress tab with statistics and analytics"""
        st.markdown("#### 📈 Learning Progress")
        st.markdown("Track your learning journey and see how you're improving")
        
        # Progress metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Questions Asked", len([m for m in st.session_state.messages if m["role"] == "user"]))
        with col2:
            st.metric("AI Responses", len([m for m in st.session_state.messages if m["role"] == "assistant"]))
        with col3:
            st.metric("Files Uploaded", len(st.session_state.uploaded_files))
        with col4:
            st.metric("Learning Level", st.session_state.user_profile['learning_level'])
        
        # Progress chart
        if st.session_state.messages:
            st.markdown("##### 📊 Daily Activity")
            # Create a simple progress chart
            progress_data = {
                "Date": [datetime.now().strftime("%Y-%m-%d")],
                "Questions": [len([m for m in st.session_state.messages if m["role"] == "user"])]
            }
            
            df = pd.DataFrame(progress_data)
            fig = px.bar(df, x="Date", y="Questions", title="Questions Asked Today")
            st.plotly_chart(fig, use_container_width=True)
        
        # Learning streaks
        st.markdown("##### 🔥 Learning Streaks")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Streak", "3 days")
        with col2:
            st.metric("Longest Streak", "7 days")
        with col3:
            st.metric("Total Days Active", "12 days")
        
        # Recent activity
        if st.session_state.messages:
            st.markdown("##### 📝 Recent Activity")
            recent_messages = st.session_state.messages[-5:]  # Last 5 messages
            for i, msg in enumerate(recent_messages):
                with st.expander(f"{'👤 You' if msg['role'] == 'user' else '🤖 AI'}: {msg['content'][:50]}..."):
                    st.write(msg['content'])
        
        # Learning goals
        st.markdown("##### 🎯 Learning Goals")
        st.info("""
        **Current Goals:**
        - Ask 10 questions this week
        - Upload 5 study materials
        - Complete 3 learning sessions
        
        **Progress:**
        - Questions: 7/10 ✅
        - Materials: 3/5 ⏳
        - Sessions: 2/3 ⏳
        """)

    def render_chat_interface(self):
        """Legacy method - now handled by render_chat_tab"""
        pass

    def authenticate_user(self, email, password):
        """Authenticate user (mock implementation)"""
        return True

    def create_user(self, name, email, password):
        """Create new user (mock implementation)"""
        return True

    def generate_ai_response(self, prompt, language, level):
        """Generate AI response using RAG"""
        try:
            # Build retrieval context from uploaded files
            context_chunks = []
            max_chars = 4000
            if st.session_state.get('uploaded_files'):
                for f in st.session_state.uploaded_files:
                    content = f.get('content')
                    if isinstance(content, bytes):
                        text = self._extract_text_from_bytes(content, f.get('name',''))
                    else:
                        text = str(content) if content is not None else ""
                    if text:
                        context_chunks.append(f"[File: {f.get('name','unknown')}]\n{text}")
                    if sum(len(c) for c in context_chunks) >= max_chars:
                        break
            context = "\n\n".join(context_chunks)[:max_chars]

            # Map selected language to engine language code
            lang_map = {
                'English': 'en',
                'Amharic': 'am',
                'Afaan Oromo': 'om',
                'Tigrigna': 'ti',
                'Yoruba': 'yo',
                'Swahili': 'sw',
            }
            # language values look like "🇺🇸 English"; take the last token(s)
            selected = language.strip()
            for label in lang_map.keys():
                if label in selected:
                    target_lang = lang_map[label]
                    break
            else:
                target_lang = 'en'

            # Ensure RAG engines are initialized if available
            if RAG_AVAILABLE and not st.session_state.get('rag_engines_initialized', False):
                self.setup_rag_engines()

            # Ensure the RAG engine exists (lazy init if needed)
            if not hasattr(self, 'multilingual_rag'):
                try:
                    from rag_engine.multilingual_rag import MultilingualRAGEngine  # lazy import
                    self.multilingual_rag = MultilingualRAGEngine()
                    st.session_state.rag_engines_initialized = True
                except Exception as e:
                    st.warning(f"RAG engine init failed: {e}")

            # Try the RAG engine if available
            if hasattr(self, 'multilingual_rag'):
                response = self.multilingual_rag.generate_multilingual_response(
                    query=prompt,
                    context=context,
                    target_language=target_lang
                )
            else:
                # Local fallback: extractive answer from uploaded file context
                if context:
                    excerpt = context[:800]
                    response = f"Here is what I found in your uploaded files related to your question:\n\n{excerpt}\n\n(Answer generated from uploaded file content. Add GROQ_API_KEY to enable full AI responses.)"
                else:
                    response = f"""
                    Thank you for your question: "{prompt}"
                    
                    I'm here to help you learn! This is a demo response. In the full implementation, 
                    I would use advanced RAG technology to provide detailed, personalized answers 
                    in your preferred language ({language}) at your learning level ({level}). If you see this, enable the AI key.
                    
                    The platform supports:
                    - Multilingual responses in 6 African languages
                    - Adaptive learning based on your level
                    - Voice input and output
                    - Progress tracking and analytics
                    - Self-validation for accuracy
                    """
            
            return response
            
        except Exception as e:
            return f"Sorry, I encountered an error: {e}. Please try again."

    def run(self):
        """Main application runner"""
        # Sync page with URL query parameter if present
        query_params = st.query_params if hasattr(st, 'query_params') else st.experimental_get_query_params()
        if query_params:
            url_page = query_params.get('page')
            if isinstance(url_page, list):
                url_page = url_page[0]
            if url_page:
                # Normalize spaces and capitalization
                url_page = url_page.replace('+', ' ')
                st.session_state.current_page = url_page

        page = st.session_state.current_page

        if not st.session_state.authenticated or st.session_state.get('show_public'):
            # Public website pages - render navigation once
            self.render_navigation()
            
            if page == "Home":
                self.render_hero_section()
                self.render_about_section()
                self.render_features_section()
                self.render_contact_section()
                self.render_footer()
            elif page == "About":
                self.render_about_section()
                self.render_footer()
            elif page == "Features":
                self.render_features_section()
                self.render_footer()
            elif page == "Contact":
                self.render_contact_section()
                self.render_footer()
            elif page == "Login" or page == "Sign Up":
                # If coming from dashboard Home, keep authenticated but show auth section if explicitly chosen
                self.render_auth_section()
            else:
                # Default to Home
                self.render_hero_section()
                self.render_about_section()
                self.render_features_section()
                self.render_contact_section()
                self.render_footer()
            # If we showed public site while authenticated, stop here
            if st.session_state.get('show_public'):
                return
        else:
            # Student dashboard after login
            self.render_dashboard()

def main():
    """Main entry point"""
    app = YenetaApp()
    app.run()

if __name__ == "__main__":
    main()
