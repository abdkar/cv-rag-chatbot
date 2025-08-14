# 🚀 RAG CVChat Pro

**Professional CV RAG Chatbot with Modular Architecture**

[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)]()
[![Architecture](https://img.shields.io/badge/Architecture-Modular-blue)]()
[![AI](https://img.shields.io/badge/AI-Google%20Gemini%202.0-orange)]()
[![Framework](https://img.shields.io/badge/Framework-Streamlit-red)]()

---

## 🎯 **Overview**

RAG CVChat Pro is a sophisticated **Retrieval Augmented Generation (RAG)** chatbot that serves as an AI-powered professional persona. Built with a **professional modular architecture**, it provides intelligent responses about your CV, experience, and professional background using Google Gemini 2.0 Flash.

### **✨ Key Features**

- 🤖 **AI-Powered Responses** - RAG pipeline with Google Gemini 2.0 Flash
- 🏗️ **Professional Architecture** - Modular, scalable, maintainable codebase
- 🖼️ **Dynamic Profile Display** - Professional photo and social links
- 📊 **Smart Knowledge Base** - Intelligent content processing and retrieval
- 🎨 **Modern UI** - Responsive Streamlit interface with custom styling
- ⚙️ **Type-Safe Configuration** - Comprehensive settings management
- 🔧 **Easy Customization** - Simple to adapt for different professionals

---

## 🏗️ **Architecture**

### **Professional Folder Structure**
```
RAG_CVChat_Pro/
├── 📱 **Applications**
│   ├── app_organized.py     ⭐ Main App (Recommended)
│   ├── app_modular.py       📜 Modular Version
│   └── app.py               📜 Original Version
│
├── 📂 **Source Code**
│   └── src/
│       ├── core/            # Business Logic
│       │   ├── embeddings.py
│       │   └── rag_pipeline.py
│       ├── ui/              # User Interface
│       │   └── components.py
│       └── utils/           # Utilities
│           └── file_processing.py
│
├── ⚙️ **Configuration**
│   └── configs/
│       └── app_config.py    # Type-safe settings
│
├── 📊 **Data**
│   ├── data/                # Knowledge base
│   ├── assets/              # Profile images
│   └── vector_store/        # AI indices
│
├── 📝 **Documentation**
│   ├── documentation/       # Detailed guides
│   └── README.md            # This file
│
└── 🚀 **Deployment**
    ├── requirements.txt     # Dependencies
    ├── Dockerfile           # Container config
    └── docker-compose.yml   # Multi-container setup
```

### **Component Responsibilities**

| Component | Purpose | Key Features |
|-----------|---------|--------------|
| **Core** | Business Logic | RAG pipeline, embeddings, AI integration |
| **UI** | User Interface | Streamlit components, styling, interactions |
| **Utils** | Support Functions | File processing, validation, caching |
| **Config** | Settings | Type-safe configuration management |

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- Google API Key (Gemini)
- Git

### **Installation**

1. **Clone Repository**
   ```bash
   git clone https://github.com/abdkar/Rag_CVChat_pro.git
   cd Rag_CVChat_pro
   ```

2. **Setup Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   # Create .env file
   echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
   ```

4. **Run Application**
   ```bash
   # Recommended: Organized version
   streamlit run app_organized.py --server.port 8511
   
   # Alternative: Modular version
   streamlit run app_modular.py --server.port 8505
   
   # Original: Monolithic version
   streamlit run app.py --server.port 8504
   ```

### **Access Your App**
- **Local**: http://localhost:8511
- **Network**: http://your-ip:8511

---

## 💡 **Usage**

### **Basic Interaction**
1. **Open the web interface**
2. **Ask questions** about professional experience
3. **Get AI-powered responses** based on your CV knowledge base
4. **Explore features** like file upload and vector source selection

### **Example Questions**
- "Tell me about your experience with machine learning"
- "What projects have you worked on recently?"
- "What are your technical skills?"
- "Describe your leadership experience"

### **Customization**
- **Knowledge Base**: Update `data/knowledge_base.txt` with your content
- **Profile**: Replace `phto.jpg` with your professional photo
- **Configuration**: Modify `configs/app_config.py` for settings
- **Styling**: Customize UI in `src/ui/components.py`

---

## 🔧 **Configuration**

### **Environment Variables**
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

### **Application Settings**
```python
# configs/app_config.py
model_name = "gemini-2.0-flash-exp"
temperature = 0.3
embedding_dimension = 384
chunk_size = 1000
```

### **UI Customization**
```python
# Social links, colors, styling
social_links = {
    "LinkedIn": "your-linkedin-url",
    "GitHub": "your-github-url",
    "Google Scholar": "your-scholar-url"
}
```

---

## 🐳 **Docker Deployment**

### **Quick Deploy**
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### **Manual Docker**
```bash
# Build image
docker build -t rag-cvchat-pro .

# Run container
docker run -p 8511:8511 --env-file .env rag-cvchat-pro
```

---

## 🧪 **Testing**

### **Component Tests**
```bash
# Test imports and basic functionality
python -c "
import sys; sys.path.append('.')
from configs.app_config import config
from src.core.embeddings import get_embeddings
from src.utils.file_processing import load_knowledge_base
print('✅ All components working!')
"
```

### **Integration Test**
```bash
# Test full pipeline
python -c "
import sys; sys.path.append('.')
from src.core.rag_pipeline import get_rag_pipeline
pipeline = get_rag_pipeline()
response = pipeline.get_response('Tell me about your experience')
print(f'✅ Pipeline working: {response[:100]}...')
"
```

---

## 📈 **Performance**

### **Optimization Features**
- ✅ **Efficient Embeddings** - Hash-based for speed and compatibility
- ✅ **Smart Caching** - Streamlit caching for expensive operations
- ✅ **Lazy Loading** - Components loaded on demand
- ✅ **Vectorized Search** - FAISS for fast similarity search

### **Benchmarks**
- **Response Time**: < 2 seconds typical
- **Memory Usage**: ~200MB baseline
- **Concurrent Users**: Supports multiple sessions

---

## 🛡️ **Security**

### **Best Practices**
- ✅ **Environment Variables** - Sensitive data in .env
- ✅ **Input Validation** - Sanitized user inputs
- ✅ **Error Handling** - Graceful failure modes
- ✅ **API Rate Limiting** - Controlled external calls

---

## 🤝 **Contributing**

### **Development Setup**
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### **Code Standards**
- **Python**: PEP 8 style guidelines
- **Documentation**: Comprehensive docstrings
- **Testing**: Unit tests for new features
- **Architecture**: Follow existing modular patterns

---

## 📋 **Dependencies**

### **Core Requirements**
- `streamlit` - Web framework
- `langchain` - RAG pipeline
- `google-generativeai` - Google Gemini API
- `faiss-cpu` - Vector similarity search
- `pypdf` - PDF processing

### **Development**
- `python-dotenv` - Environment management
- `dataclasses` - Type-safe configuration

---

## 📚 **Documentation**

### **Detailed Guides**
- [Architecture Overview](documentation/PROJECT_STRUCTURE.md)
- [Configuration Guide](documentation/CONFIGURATION.md)
- [Deployment Guide](documentation/DEPLOYMENT.md)
- [Customization Guide](documentation/CUSTOMIZATION.md)

### **API Reference**
- [Core Components](src/core/README.md)
- [UI Components](src/ui/README.md)
- [Utilities](src/utils/README.md)

---

## 🏆 **Features Comparison**

| Feature | Basic | Professional | Enterprise |
|---------|-------|--------------|------------|
| **RAG Pipeline** | ✅ | ✅ | ✅ |
| **Modular Architecture** | ❌ | ✅ | ✅ |
| **Professional UI** | ❌ | ✅ | ✅ |
| **Docker Support** | ❌ | ✅ | ✅ |
| **Multi-user** | ❌ | ❌ | ✅ |
| **Analytics** | ❌ | ❌ | ✅ |

**This is the Professional version** 🎯

---

## 🚀 **Roadmap**

### **v2.0 - Advanced Features**
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Plugin architecture
- [ ] Database integration

### **v3.0 - Enterprise**
- [ ] Multi-user management
- [ ] API endpoints
- [ ] Advanced security
- [ ] Microservices architecture

---

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 **Author**

**Abdolamir Karbalaie**
- LinkedIn: [abdolamir-karbalaie](https://www.linkedin.com/in/abdolamir-karbalaie-3bab9451/)
- GitHub: [@abdkar](https://github.com/abdkar)
- Google Scholar: [Profile](https://scholar.google.com/citations?user=Noi7TFUAAAA)

---

## 🙏 **Acknowledgments**

- **Google Gemini** - Advanced AI capabilities
- **Streamlit** - Excellent web framework
- **LangChain** - RAG pipeline infrastructure
- **FAISS** - Efficient vector search

---

## 📞 **Support**

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/abdkar/Rag_CVChat_pro/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/abdkar/Rag_CVChat_pro/discussions)
- 📧 **Direct Contact**: [Email](mailto:contact@example.com)

---

## 📊 **Stats**

![GitHub Stars](https://img.shields.io/github/stars/abdkar/Rag_CVChat_pro)
![GitHub Forks](https://img.shields.io/github/forks/abdkar/Rag_CVChat_pro)
![GitHub Issues](https://img.shields.io/github/issues/abdkar/Rag_CVChat_pro)
![GitHub License](https://img.shields.io/github/license/abdkar/Rag_CVChat_pro)

---

*Professional CV RAG Chatbot - Built with ❤️ using modern AI and clean architecture*
