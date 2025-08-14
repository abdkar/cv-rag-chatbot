#  CV RAG Chatbot - Professional AI Assistant

[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)]()
[![Architecture](https://img.shields.io/badge/Architecture-Modular-blue)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

###  AI & ML Stack
[![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange)]()
[![LangChain](https://img.shields.io/badge/LangChain-0.2.10+-blue)]()
[![RAG](https://img.shields.io/badge/RAG-FAISS%20Vector%20Store-purple)]()
[![Embeddings](https://img.shields.io/badge/Embeddings-HuggingFace-yellow)]()

### 🖥️ Frontend & UI
[![Framework](https://img.shields.io/badge/Framework-Streamlit-red)]()
[![CSS3](https://img.shields.io/badge/CSS3-Glass%20Morphism-blue)]()
[![Animations](https://img.shields.io/badge/Animations-CSS3%20Keyframes-green)]()
[![Icons](https://img.shields.io/badge/Icons-Authentic%20SVG-lightblue)]()

###  Backend & Infrastructure
[![Python](https://img.shields.io/badge/Python-3.8+-blue)]()
[![Vector DB](https://img.shields.io/badge/Vector%20DB-FAISS-darkgreen)]()
[![Environment](https://img.shields.io/badge/Environment-dotenv-lightgreen)]()
[![API](https://img.shields.io/badge/API-Google%20Generative%20AI-orange)]()

###  Deployment & DevOps
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue)]()
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-Multi%20Service-lightblue)]()
[![Testing](https://img.shields.io/badge/Testing-Automated%20System%20Tests-green)]()
[![Git](https://img.shields.io/badge/Git-Version%20Control-red)]()

###  Key Dependencies
[![Streamlit](https://img.shields.io/badge/streamlit-1.28.0+-red)]()
[![LangChain Community](https://img.shields.io/badge/langchain--community-0.2.10+-blue)]()
[![FAISS CPU](https://img.shields.io/badge/faiss--cpu-1.7.0+-purple)]()
[![Google GenAI](https://img.shields.io/badge/google--generativeai-0.7.0+-orange)]()
[![PyPDF](https://img.shields.io/badge/pypdf-3.0.0+-darkgreen)]()

> A production-ready CV/Resume chatbot with intelligent RAG (Retrieval-Augmented Generation) capabilities, beautiful UI, and smart quota management.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment variables
cp .env.template .env
# Edit .env file and add your GOOGLE_API_KEY

# 3. Test the system (recommended)
python test_system.py

# 4. Run the application
streamlit run app_smart.py --server.port=8511 --server.address=0.0.0.0
```

**Access:** http://localhost:8511

**🧪 Test Everything:** Run `python test_system.py` to verify all components work correctly

## 📁 Project Structure

```
CV_RAG_OP/
├── 📱 app_smart.py              # Main application (production-ready)
├── 📱 app.py                    # Original base application  
├── 📊 knowledge_base.txt        # Professional knowledge content
├── ⚙️ requirements.txt          # Python dependencies
├── 🔑 .env.template             # Environment variables template
├── 🧪 test_system.py            # Complete system testing script
├── ⚙️ configs/                  # Configuration management
├── 🧠 src/                      # Core application modules
│   ├── core/                    # RAG pipeline and embeddings
│   ├── ui/                      # UI components and styling
│   └── utils/                   # Utility functions
├── 🗂️ vector_store/             # FAISS vector indices (auto-generated)
├── 🎨 assets/                   # Images and static files
├── 📚 docs/                     # All documentation files
├── 🚀 deployment/               # Docker and deployment files
├── 📦 archive/                  # Old versions and backups
├── 🔧 scripts/                  # Setup and utility scripts
└── 📊 logs/                     # Application logs
```

## ✨ Features

- **🎨 Beautiful UI** - Modern glass morphism design with animations
- **🤖 Smart AI Chat** - RAG-powered responses with professional context  
- **🔄 Intelligent Quota Management** - Automatic API fallback and monitoring
- **🔍 Semantic Search** - FAISS-powered vector search through knowledge base
- **🎯 Professional Focus** - Specialized for CV/Resume and career discussions
- **🛡️ Production Ready** - Error handling, security, environment management

## 🔧 Technical Stack

- **Frontend:** Streamlit with custom CSS3 animations and glass morphism
- **AI Model:** Google Gemini (gemini-1.5-flash-8b - working model)
- **Vector Store:** FAISS with HuggingFace sentence-transformers embeddings
- **Knowledge Base:** Comprehensive professional CV content (AI safety, publications)
- **Architecture:** Modular RAG pipeline with intelligent quota management

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+ 
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Internet connection for API calls

### Step-by-Step Setup
1. **Clone and navigate:**
   ```bash
   cd CV_RAG_OP
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment:**
   ```bash
   cp .env.template .env
   # Edit .env and add: GOOGLE_API_KEY=your_actual_api_key_here
   ```

4. **Test everything (recommended):**
   ```bash
   python test_system.py
   ```

5. **Run the application:**
   ```bash
   streamlit run app_smart.py --server.port=8511 --server.address=0.0.0.0
   ```

6. **Open browser:** http://localhost:8511

## 🧪 Testing & Troubleshooting

### Complete System Test
```bash
python test_system.py
```
This comprehensive test script will:
- ✅ Check all dependencies
- ✅ Validate project structure  
- ✅ Test API connectivity
- ✅ Verify RAG pipeline
- ✅ Test UI components
- ✅ Provide detailed troubleshooting

### Common Issues & Quick Fixes

| Problem | Solution |
|---------|----------|
| **Missing dependencies** | `pip install -r requirements.txt` |
| **No API key** | Get key from [Google AI Studio](https://makersuite.google.com/app/apikey), add to `.env` |
| **API quota exceeded** | App has built-in quota management, or wait for reset |
| **Port in use** | Use different port: `--server.port=8512` |
| **Import errors** | Check Python version (3.8+), activate virtual environment |
| **Vector store issues** | Delete `vector_store/` directory (auto-rebuilds) |

### Manual Testing
```bash
# Test API connectivity
python -c "
from configs.app_config import get_google_api_key
import google.generativeai as genai
genai.configure(api_key=get_google_api_key())
model = genai.GenerativeModel('gemini-1.5-flash-8b')
print('✅ API Working:', model.generate_content('Hello').text)
"

# Test imports
python -c "
import streamlit, langchain, faiss
from src.core.rag_pipeline import RAGPipeline
print('✅ All imports successful')
"
```

## 📖 Documentation

- **[Complete System Test](test_system.py)** - Comprehensive testing and troubleshooting script
- **[Project Organization](docs/PROJECT_ORGANIZATION.md)** - File structure and organization
- **[Deployment Guide](docs/DEPLOYMENT_BACKUP_GUIDE.md)** - Production deployment instructions
- **[Final Project Summary](docs/FINAL_PROJECT_SUMMARY.md)** - Complete feature overview
- **[Knowledge Base Guide](docs/KNOWLEDGE_BASE_UPDATE_GUIDE.md)** - How to update content

## 🎯 Current Status

✅ **Production Ready** - Fully functional with intelligent quota management  
✅ **Beautiful Design** - Professional UI with animations and authentic platform icons  
✅ **Smart Fallbacks** - Graceful degradation and error handling  
✅ **Complete Testing** - Comprehensive test script for validation  
✅ **Clean Organization** - Professional file structure and documentation  

## 🚨 Important Notes

- **API Key Required:** You must have a valid Google Gemini API key
- **Internet Required:** App needs internet connection for AI responses
- **Model Dependency:** Currently uses `gemini-1.5-flash-8b` (confirmed working)
- **Port Flexibility:** Default port 8511, can be changed if needed
- **Auto-Generation:** Vector store and embeddings are created automatically on first run

---

*Last Updated: August 14, 2025*  
*Status: Production Ready ✅*  
*Testing: Comprehensive test script available ✅*
