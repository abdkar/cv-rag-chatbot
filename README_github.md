# CV RAG Chatbot - AI-Powered Professional Assistant

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.48+-red)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-green)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-2.0_Flash-orange)

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

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/cv-rag-chatbot.git
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

## 📁 Project Structure

```
cv-rag-chatbot/
├── app.py                 # Main Streamlit application
├── knowledge_base.txt     # CV/Resume content
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore file
├── README.md             # This file
├── phto.jpg              # Profile photo
├── assets/               # Additional assets
├── documentation/        # Project documentation
├── logs/                 # Application logs
└── vector_store/         # FAISS vector database
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
- **Vector Database**: FAISS with HuggingFace embeddings
- **File Processing**: PyPDF for PDF handling
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
- HuggingFace embeddings (all-MiniLM-L6-v2)
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
```bash
streamlit run app.py --server.headless true --server.address 0.0.0.0 --server.port 8501
```

## 🧪 Testing

Run the health check script:
```bash
python health_check.py
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
