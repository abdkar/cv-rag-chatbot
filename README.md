# CV RAG Chatbot - AI-Powered Professional Assistant

![python](https://img.shields.io/badge/python-3.9+-blue.svg)
![streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![langchain](https://img.shields.io/badge/langchain-0.2+-green.svg)
![gemini](https://img.shields.io/badge/Google%20Gemini-2.0%20Flash-blue.svg)
![faiss](https://img.shields.io/badge/FAISS-vector%20db-orange.svg)
![docker](https://img.shields.io/badge/docker-ready-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A sophisticated AI-powered chatbot that answers questions about your CV/Resume using Retrieval Augmented Generation (RAG) technology with Google Gemini 2.0 Flash integration.

## 🌟 Features

- **🤖 Advanced AI Integration**: Google Gemini 2.0 Flash for natural conversations
- **🎯 RAG Technology**: Grounded responses from actual CV content
- **🎨 Beautiful Interface**: Professional UI with dark blue theme and profile photo
- **📚 Smart Content Management**: Dual vector stores for base and uploaded content
- **🔒 Secure Validation**: Name verification for uploaded content
- **📱 Responsive Design**: Works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Google Gemini API key
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/abdkar/cv-rag-chatbot.git
cd cv-rag-chatbot
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment:**
```bash
# Create .env file
echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
```

4. **Run the application:**
```bash
streamlit run app.py
```

5. **Access the app:**
Open http://localhost:8501 in your browser

## � Docker Deployment

### Quick Docker Start

1. **Using Docker Compose (Recommended):**
```bash
# Clone the repository
git clone https://github.com/abdkar/cv-rag-chatbot.git
cd cv-rag-chatbot

# Set up environment
echo "GOOGLE_API_KEY=your_google_api_key_here" > .env

# Deploy with Docker
./docker-deploy.sh deploy
```

2. **Manual Docker Build:**
```bash
# Build the image
docker build -t cv-rag-chatbot .

# Run the container
docker run -p 8501:8501 --env-file .env cv-rag-chatbot
```

### Docker Commands

```bash
# Deploy application
./docker-deploy.sh deploy

# View logs
./docker-deploy.sh logs

# Stop application
./docker-deploy.sh stop

# Check status
./docker-deploy.sh status

# Full cleanup
./docker-deploy.sh cleanup
```

## �📁 Project Structure

```
cv-rag-chatbot/
├── app.py                 # Main Streamlit application
├── knowledge_base.txt     # CV/Resume content
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore file
├── README.md             # This file
├── LICENSE               # MIT License file
├── phto.jpg              # Profile photo
├── Dockerfile            # Docker container configuration
├── docker-compose.yml    # Docker Compose configuration
├── docker-deploy.sh      # Docker deployment script
├── .dockerignore         # Docker ignore file
├── health_check.py       # Application health monitoring
├── setup.py              # Setup and installation script
├── assets/               # Additional assets and resources
├── documentation/        # Project documentation
├── logs/                 # Application logs directory
├── vector_store/         # FAISS vector database storage
├── backups/              # Backup files and configurations
├── test_files/           # Test data and examples
└── unused_files/         # Archived and unused components
```

## 💡 Usage

### Basic Chat
1. Open the application in your browser
2. Ask questions about the CV content
3. Get AI-powered responses grounded in the knowledge base

### File Upload
1. Use the sidebar to upload new CV/Resume files (PDF or TXT)
2. Content is validated for authenticity
3. Switch between base knowledge and uploaded content

### Example Questions
- "What is your experience in machine learning?"
- "Tell me about your educational background"
- "Describe your leadership experience"
- "What programming languages do you know?"

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS
- **AI Model**: Google Gemini 2.0 Flash
- **Framework**: LangChain for RAG pipeline
- **Vector Database**: FAISS with custom hash-based embeddings
- **File Processing**: PyPDF for PDF handling
- **Containerization**: Docker with Docker Compose
- **Styling**: Custom CSS with responsive design

## 🔧 Configuration

### Environment Variables
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

### Customization
- Replace `knowledge_base.txt` with your CV content
- Update `phto.jpg` with your profile photo
- Modify the name validation in the code for your name

## 📊 Features in Detail

### RAG Pipeline
- Text chunking with RecursiveCharacterTextSplitter
- Custom hash-based embeddings for maximum compatibility
- FAISS vector store for semantic search
- Custom prompt templates for natural responses

### UI Components
- Profile section with photo and social links
- Chat interface with message history
- File upload with validation
- Quick start question buttons
- Vector source switching

### Security
- API key protection via environment variables
- Content validation for uploaded files
- Safe file handling for PDF/TXT uploads

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment

#### Using Docker (Recommended)
```bash
# Production deployment with Docker
./docker-deploy.sh deploy

# Monitor application
./docker-deploy.sh status
./docker-deploy.sh logs
```

#### Manual Production Setup
```bash
# Install production dependencies
pip install -r requirements.txt

# Run with production settings
streamlit run app.py \
  --server.headless true \
  --server.address 0.0.0.0 \
  --server.port 8501 \
  --server.enableCORS false \
  --server.enableXsrfProtection true
```

#### Cloud Deployment
The Docker container can be deployed to any cloud platform:
- **AWS**: ECS, EC2, or Lambda
- **Google Cloud**: Cloud Run, GKE, or Compute Engine  
- **Azure**: Container Instances or App Service
- **Heroku**: Container deployment
- **DigitalOcean**: App Platform or Droplets

## 🧪 Testing

### Health Check
Run the comprehensive health check script to verify all components:
```bash
python health_check.py
```

This script checks:
- **Environment Setup**: API keys and configuration
- **Dependencies**: All required packages installed
- **File Structure**: Essential files present  
- **Application Health**: Streamlit functionality
- **Docker Status**: Container health (if running)

### Manual Testing
```bash
# Test the application directly
streamlit run app.py

# Test Docker deployment
./docker-deploy.sh deploy
./docker-deploy.sh status
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Contact

**Abdolamir Karbalaie**
- LinkedIn: [abdolamir-karbalaie](https://www.linkedin.com/in/abdolamir-karbalaie-3bab9451/)
- GitHub: [@abdkar](https://github.com/abdkar)
- Google Scholar: [Profile](https://scholar.google.com/citations?user=Noi7TFUAAAA)

## 🙏 Acknowledgments

- Google for Gemini API
- Streamlit team for the amazing framework
- LangChain for RAG capabilities
- HuggingFace for embeddings

---

**Made with ❤️ using AI and RAG technology**
