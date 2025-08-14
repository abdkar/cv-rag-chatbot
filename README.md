# 🤖 CV RAG Chatbot - Professional AI Assistant

[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)]()
[![Architecture](https://img.shields.io/badge/Architecture-Modular-blue)]()
[![AI](https://img.shields.io/badge/AI-Google%20Gemini%202.0-orange)]()
[![Framework](https://img.shields.io/badge/Framework-Streamlit-red)]()


> A production-ready CV/Resume chatbot with intelligent RAG (Retrieval-Augmented Generation) capabilities, beautiful UI, and smart quota management.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.template .env
# Add your GOOGLE_API_KEY to .env

# Run the application
streamlit run app_smart.py --server.port=8511 --server.address=0.0.0.0
```

**Access:** http://localhost:8511

## 📁 Project Structure

```
CV_RAG_OP/
├── 📱 app_smart.py              # Main application (production-ready)
├── 📱 app.py                    # Original base application
├── ⚙️ configs/                  # Configuration management
├── 🧠 src/                      # Core application modules
│   ├── core/                    # RAG pipeline and embeddings
│   ├── ui/                      # UI components and styling
│   └── utils/                   # Utility functions
├── 📊 knowledge_base.txt        # Professional knowledge content
├── 🗂️ vector_store/             # FAISS vector indices
├── 🎨 assets/                   # Images and static files
├── 📚 docs/                     # Documentation
├── 🚀 deployment/               # Docker and deployment files
├── 📦 archive/                  # Old versions and backups
└── 🔧 scripts/                  # Setup and utility scripts
```

## ✨ Features

- **🎨 Beautiful UI** - Modern glass morphism design with animations
- **🤖 Smart AI Chat** - RAG-powered responses with professional context  
- **🔄 Intelligent Quota Management** - Automatic API fallback and monitoring
- **🔍 Semantic Search** - FAISS-powered vector search through knowledge base
- **🎯 Professional Focus** - Specialized for CV/Resume and career discussions
- **🛡️ Production Ready** - Error handling, security, environment management

## 🔧 Technical Stack

- **Frontend:** Streamlit with custom CSS animations
- **AI Model:** Google Gemini (gemini-1.5-flash-8b)
- **Vector Store:** FAISS with hash-based embeddings
- **Knowledge Base:** Comprehensive professional content
- **Architecture:** Modular RAG pipeline with smart fallbacks

## 📖 Documentation

- **[Complete Project Summary](docs/FINAL_PROJECT_SUMMARY.md)** - Full feature overview
- **[Deployment Guide](docs/DEPLOYMENT_BACKUP_GUIDE.md)** - Production deployment
- **[Architecture Details](docs/)** - Technical documentation

## 🎯 Current Status

✅ **Production Ready** - Fully functional with intelligent quota management  
✅ **Beautiful Design** - Professional UI with animations and authentic icons  
✅ **Smart Fallbacks** - Graceful degradation and error handling  
✅ **Complete Documentation** - Comprehensive guides and procedures  

---

*Last Updated: August 14, 2025*  
*Status: Production Ready ✅*
