### 🌍 Yeneta — Multilingual AI Study Platform
Bridging educational gaps across Africa with advanced, multilingual RAG.

[![RAG](https://img.shields.io/badge/RAG-Advanced%20Pipeline-2b6cb0)](https://langchain.com)
[![Languages](https://img.shields.io/badge/Languages-6-green)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

### ✨ Overview
Yeneta is a multilingual AI tutoring platform powered by Retrieval-Augmented Generation (RAG). It personalizes learning, works in six African languages, supports voice interactions, and adapts to each learner’s level.

---

### 📚 Table of Contents
- **[Features](#-features)**
- **[Architecture](#-architecture)**
- **[Folder Structure](#-folder-structure)**
- **[Quick Start](#-quick-start)**
- **[Configuration](#-configuration)**
- **[Development](#-development)**
- **[Roadmap](#-roadmap)**
- **[Contributing](#-contributing)**
- **[Acknowledgments](#-acknowledgments)**

---

### 🔑 Features
- **Multilingual RAG**: Detects input language and responds appropriately (Amharic, Afaan Oromo, Tigrigna, English, Yoruba, Swahili).
- **Adaptive Learning**: Calibrates difficulty (beginner → advanced) using learner context and memory.
- **Hybrid Retrieval**: Semantic + keyword + reranking for robust accuracy.
- **Memory-Augmented Responses**: Remembers progress, weak topics, and goals.
- **Voice Accessibility**: Speech-to-text and text-to-speech support.
- **Analytics**: Progress tracking, insights, and recommendations.

---

### 🏗️ Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                         YENETA                               │
├─────────────────────────────────────────────────────────────┤
│  UI: Streamlit                                               │
│  ├─ Multilingual UI  ├─ Voice I/O  ├─ Progress Dashboard     │
├─────────────────────────────────────────────────────────────┤
│  RAG Engine (Python)                                         │
│  ├─ Multilingual RAG  ├─ Adaptive RAG  ├─ Reflective RAG     │
│  ├─ Memory RAG        ├─ Hybrid Search (semantic+BM25)       │
├─────────────────────────────────────────────────────────────┤
│  Persistence & Services                                      │
│  ├─ ChromaDB (vectors)  ├─ Supabase (auth, data)             │
└─────────────────────────────────────────────────────────────┘
```

---

### 🗂️ Folder Structure
```text
app.py                         # Streamlit application entry point
auth/                          # Authentication (Supabase helpers)
chroma_store/                  # Local ChromaDB store (ephemeral)
config/                        # App and Supabase configuration
database/                      # SQL schemas / migrations
demo_data/                     # Sample content and questions
features/                      # Platform feature modules
rag_engine/                    # Core RAG implementations
run_demo.py                    # Demo launcher
requirements.txt               # Python dependencies
README.md                      # This file
```

---

### 🚀 Quick Start
Prerequisites:
```bash
Python 3.10+
GROQ_API_KEY 
SUPABASE_URL and SUPABASE_ANON_KEY
```

Installation:
```bash
git clone https://github.com/your-username/yeneta.git
cd yeneta

python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

### ⚙️ Configuration
Create a `.env` file (or set environment variables through your OS):
```bash
GROQ_API_KEY=...
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
```

Supabase schema lives in `database/supabase_schema.sql`.

---

### 🧑‍💻 Development
- **Code Style**: Prefer readable, well-named variables and functions.
- **Virtual Env**: Use an isolated environment (`.venv`).
- **Data Stores**: `chroma_store/` is ephemeral; do not commit large DB files.
- **Temp/Uploads**: `temp_files/` and `uploaded_files/` are safe to clear.

Run demo:
```bash
python run_demo.py
```

---

### 🗺️ Roadmap
- Add more local languages and dialect support
- Expand analytics and teacher dashboards
- Mobile-first UI improvements
- Dataset ingestion pipeline for institutions

---

### 🤝 Contributing
Contributions are welcome!
1. Fork the repo and create a feature branch.
2. Make changes with clear commits.
3. Open a pull request with context and screenshots where applicable.

---
 

### 🙏 Acknowledgments
- LangChain — RAG framework and components
- Groq — Fast LLM inference
- African language communities — Linguistic guidance and validation

— Empowering learners with accessible, culturally-aware AI.
