"""
🚀 Yeneta Platform Runner
Quick setup and platform script for Yeneta

This script helps you quickly set up and run the Yeneta platform
"""

import os
import sys
import subprocess
import streamlit as st

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        "streamlit",
        "langchain",
        "langchain-groq",
        "chromadb",
        "sentence-transformers"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def setup_environment():
    """Set up environment variables"""
    print("🔧 Setting up environment...")
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("📝 Creating .env file...")
        with open(".env", "w") as f:
            f.write("""# Yeneta Environment Configuration
# Add your API keys here

# Groq API Key (Required)
GROQ_API_KEY=your_groq_api_key_here

# Supabase Configuration (Optional for platform)
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here

# Application Settings
APP_NAME=Yeneta
APP_VERSION=1.0.0
DEBUG=True
LOG_LEVEL=INFO

# RAG Configuration
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CROSS_ENCODER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2
CHROMA_PERSIST_DIRECTORY=./chroma_store

# Language Configuration
SUPPORTED_LANGUAGES=am,om,ti,en,yo,sw
DEFAULT_LANGUAGE=en

# Voice Configuration
VOICE_ENABLED=True
TTS_LANGUAGE=en
STT_LANGUAGE=en

# File Upload Configuration
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=pdf,docx,txt,md

# Security Configuration
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_here
""")
        print("✅ .env file created!")
        print("⚠️  Please add your GROQ_API_KEY to the .env file")
    else:
        print("✅ .env file already exists")

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "chroma_store",
        "uploaded_files",
        "temp_files",
        "logs"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created {directory}/")
        else:
            print(f"✅ {directory}/ already exists")

def run_platform():
    """Run the Yeneta platform"""
    print("🚀 Starting Yeneta Platform...")
    print("🌍 Multilingual AI Study Platform")
    print("🚀 Advanced RAG Implementation")
    print("-" * 50)
    
    try:
        # Run Streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Platform stopped by user")
    except Exception as e:
        print(f"❌ Error running platform: {e}")

def main():
    """Main platform setup function"""
    print("🌍 YENETA - Multilingual AI Study Platform")
    print("🚀 Advanced RAG Implementation for Educational Excellence")
    print("=" * 60)
    
    # Check requirements
    print("\n1. Checking requirements...")
    missing = check_requirements()
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("📦 Installing requirements...")
        if not install_requirements():
            print("❌ Failed to install requirements. Please install manually:")
            print(f"pip install {' '.join(missing)}")
            return
    else:
        print("✅ All requirements satisfied!")
    
    # Setup environment
    print("\n2. Setting up environment...")
    setup_environment()
    
    # Create directories
    print("\n3. Creating directories...")
    create_directories()
    
    # Check API key
    print("\n4. Checking configuration...")
    if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "your_groq_api_key_here":
        print("⚠️  GROQ_API_KEY not set!")
        print("📝 Please add your Groq API key to the .env file")
        print("🔗 Get your API key at: https://console.groq.com/keys")
        
        api_key = input("\nEnter your Groq API key (or press Enter to skip): ").strip()
        if api_key:
            # Update .env file
            with open(".env", "r") as f:
                content = f.read()
            content = content.replace("GROQ_API_KEY=your_groq_api_key_here", f"GROQ_API_KEY={api_key}")
            with open(".env", "w") as f:
                f.write(content)
            print("✅ API key saved!")
        else:
            print("⚠️  Platform will run without API key (limited functionality)")
    else:
        print("✅ API key configured!")
    
    # Run platform
    print("\n5. Starting platform...")
    print("🎯 Features to showcase:")
    print("   • Multilingual RAG (6 African languages)")
    print("   • Adaptive RAG (learning level adjustment)")
    print("   • Self-Reflective RAG (educational validation)")
    print("   • Memory-Augmented RAG (personalized learning)")
    print("   • Voice processing (accessibility)")
    print("   • Progress tracking and analytics")
    
    input("\nPress Enter to start the platform...")
    run_platform()

if __name__ == "__main__":
    main()
