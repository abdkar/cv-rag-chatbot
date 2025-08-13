import streamlit as st
import os
import base64
from dotenv import load_dotenv
from datetime import datetime
import hashlib
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

@st.cache_resource
def initialize_embeddings():
    """Initialize embeddings model with caching and PyTorch meta tensor workaround"""
    try:
        st.info("Loading embeddings model... This may take a moment on first run.")
        
        # Workaround for PyTorch meta tensor issues
        import os
        os.environ["TORCH_DISABLE_META_TENSOR"] = "1"
        os.environ["PYTORCH_DISABLE_META_TENSOR"] = "1"
        
        import torch
        # Clear GPU cache and force CPU
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        torch.set_default_device('cpu')
        
        # Try with specific PyTorch settings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={
                'device': 'cpu',
                'torch_dtype': torch.float32
            },
            encode_kwargs={'normalize_embeddings': False}  # Disable normalization to avoid meta tensor issues
        )
        st.success("✅ Primary embeddings model loaded successfully!")
        return embeddings
        
    except Exception as e:
        st.warning(f"⚠️ Primary model failed: Meta tensor issue detected")
        st.info("🔄 Switching to lightweight embeddings approach...")
        
        # Use a completely different approach that avoids PyTorch meta tensors
        try:
            class SimpleEmbeddings:
                def __init__(self):
                    from sentence_transformers import SentenceTransformer
                    import torch
                    
                    # Force CPU and disable meta tensors completely
                    torch.set_default_device('cpu')
                    with torch.no_grad():
                        self.model = SentenceTransformer(
                            'all-MiniLM-L6-v2',
                            device='cpu',
                            cache_folder='./.cache'
                        )
                
                def embed_documents(self, texts):
                    import torch
                    with torch.no_grad():
                        embeddings = self.model.encode(
                            texts, 
                            convert_to_numpy=True,
                            show_progress_bar=False
                        )
                    return embeddings.tolist()
                
                def embed_query(self, text):
                    import torch
                    with torch.no_grad():
                        embedding = self.model.encode(
                            [text], 
                            convert_to_numpy=True,
                            show_progress_bar=False
                        )
                    return embedding[0].tolist()
            
            embeddings = SimpleEmbeddings()
            st.success("✅ Lightweight embeddings loaded successfully!")
            return embeddings
            
        except Exception as e2:
            st.error(f"❌ Lightweight approach failed: {str(e2)}")
            st.info("🔄 Trying minimal embeddings...")
            
            # Ultra-simple fallback that should always work
            try:
                class MinimalEmbeddings:
                    def __init__(self):
                        # Use a very simple approach
                        import sentence_transformers
                        self.model = sentence_transformers.SentenceTransformer(
                            'paraphrase-MiniLM-L3-v2',  # Smaller, more compatible model
                            device='cpu'
                        )
                    
                    def embed_documents(self, texts):
                        return self.model.encode(texts, convert_to_numpy=True).tolist()
                    
                    def embed_query(self, text):
                        return self.model.encode([text], convert_to_numpy=True)[0].tolist()
                
                embeddings = MinimalEmbeddings()
                st.success("✅ Minimal embeddings loaded successfully!")
                return embeddings
                
            except Exception as e3:
                st.error(f"❌ All embeddings approaches failed")
                st.error("🔧 Please try running locally instead of Docker, or restart the container")
                st.info("💡 This appears to be a PyTorch/Docker compatibility issue")
                st.stop()

def extract_pdf_text(uploaded_file):
    """Extract text from PDF file using pypdf"""
    try:
        from pypdf import PdfReader
        
        # Reset file pointer to beginning
        uploaded_file.seek(0)
        
        reader = PdfReader(uploaded_file)
        text = ""
        
        for page_num, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            except Exception as e:
                st.warning(f"Could not extract text from page {page_num + 1}: {str(e)}")
                continue
        
        if not text.strip():
            raise Exception("No text could be extracted from the PDF")
            
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting PDF text: {str(e)}")

# Configure Streamlit page
st.set_page_config(
    page_title="CV Chatbot", 
    page_icon="💼", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_kb_hash():
    """Get hash of current knowledge base for caching."""
    try:
        with open("knowledge_base.txt", "r", encoding="utf-8") as f:
            content = f.read()
        return hashlib.md5(content.encode()).hexdigest()
    except FileNotFoundError:
        return "no_file"

@st.cache_resource
def validate_name_in_content(content: str) -> bool:
    """Check if the content contains Abdolamir Karbalaie"""
    name_variations = [
        "Abdolamir Karbalaie",
        "abdolamir karbalaie", 
        "ABDOLAMIR KARBALAIE",
        "Abdolamir",
        "Karbalaie"
    ]
    content_lower = content.lower()
    return any(name.lower() in content_lower for name in name_variations)

def load_rag_pipeline(kb_hash: str, use_uploaded: bool = False):
    """Load and cache the RAG pipeline."""
    try:
        # Always read knowledge base as primary source
        with open("knowledge_base.txt", "r", encoding="utf-8") as f:
            base_content = f.read()
            
        # Check if we should use uploaded file content
        content_to_use = base_content
        if use_uploaded and os.path.exists("uploaded_content.txt"):
            with open("uploaded_content.txt", "r", encoding="utf-8") as f:
                uploaded_content = f.read()
                if validate_name_in_content(uploaded_content):
                    content_to_use = uploaded_content
                else:
                    st.warning("⚠️ Uploaded content doesn't contain your name. Using knowledge base instead.")
        
        cv_content = content_to_use
        
    except FileNotFoundError:
        st.error("❌ knowledge_base.txt not found!")
        return None
    
    # Configure Google AI
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # Initialize LLM
    llm = GoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3,
        timeout=15
    )
    
    # Split text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(cv_content)
    
    # Create embeddings with cached initialization
    embeddings = initialize_embeddings()
    
    # Create vector store
    vectorstore = FAISS.from_texts(chunks, embeddings)
    
    # Create custom prompt template for more natural responses
    template = """
    You are the professional AI persona of Abdolamir (“Amir”) Karbalaie. Use ONLY the Context. Do not invent or speculate.
    
    Write naturally and concisely in third person (“he”). Do not say “according to the context.” Quantify only when numbers appear in the Context.
    
    If the question is identity/overview (e.g., “who is…”, “tell me about…”), produce a polished 2–3 sentence paragraph. Otherwise, write one direct opening sentence followed by 3 compact bullets with **Bold labels** (≤2 words) and a colon.
    
    If the needed facts are missing: “I do not have that information in the current context.”
    If the question is personal/out-of-scope (contact, family, salary, religion, politics):
    “I do not have information on that topic. For details, it would be best to speak with Abdolamir directly.”
    
    Context
    {context}
    
    Question
    {question}

    Answer:
    """
    
    # Vector Source
    custom_prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )



    # Create QA chain with custom prompt
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=False,
        verbose=False,
        chain_type_kwargs={"prompt": custom_prompt}
    )
    
    built_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"chain": qa_chain, "kb_hash": kb_hash, "built_at": built_at}

# Inject CSS styles
def _inject_css():
    # Get profile image as base64 - try both locations
    banner_b64 = ""
    profile_paths = ["phto.jpg", "assets/profile.jpg"]
    
    for profile_path in profile_paths:
        try:
            with open(profile_path, "rb") as f:
                banner_b64 = base64.b64encode(f.read()).decode()
                break
        except Exception:
            continue
    
    css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"]  {{ font-family: 'Inter', sans-serif; }}
.block-container {{ max-width: 1400px !important; padding-top: 1rem !important; padding-bottom: 2rem !important; }}
body {{ background: linear-gradient(120deg, #f5f9ff 0%, #eef3fa 55%, #e6edf5 100%); }}
body {{ 
    background: linear-gradient(120deg, #f5f9ff 0%, #eef3fa 55%, #e6edf5 100%); 
}}

/* Enhanced main container with proper spacing */
.main .block-container {{
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 1.5rem;
    margin-top: 0.5rem;
    box-shadow: 0 8px 24px -6px rgba(32,60,120,0.25), 0 4px 12px rgba(32,60,120,0.12);
    border: 1px solid #d4e0ef;
}}

/* Keep footer hidden but show deploy button */
footer {{ visibility: hidden !important; }}

.hero-wrapper {{ margin: 0.4rem auto 1.2rem auto; }}
.hero-card, .hero-card * {{
    background-color: #003147 !important;
    background-image: none !important;
    background: #003147 !important;
}}
.hero-card {{
    width: 100%; 
    min-height: 300px;
    background: #003147 !important;
    backdrop-filter: blur(15px);
    border: 1px solid #003147; 
    border-radius: 24px; 
    padding: 2rem; 
    position: relative; 
    overflow: hidden;
    box-shadow: 0 8px 24px -6px rgba(0, 49, 71, 0.25), 0 4px 12px rgba(0, 49, 71, 0.12);
    display: flex;
    align-items: center;
    gap: 2rem;
}}

.hero-card:before {{
    content: "";
    position: absolute;
    inset: 0;
    background: transparent;
    z-index: 1;
}}

.profile-photo {{
    width: 180px;
    height: 180px;
    border-radius: 50%;
    background: url(data:image/jpeg;base64,{banner_b64}) center top 15px/cover no-repeat;
    border: 4px solid rgba(255,255,255,0.8);
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    position: relative;
    z-index: 2;
    flex-shrink: 0;
}}

.hero-content {{
    position: relative;
    z-index: 2;
    flex: 1;
}}

.role-chips {{
    margin-bottom: 1rem;
}}

.role-chip {{ 
    display: inline-block; 
    background: rgba(255, 255, 255, 0.15); 
    color: white; 
    font-size: 0.7rem; 
    font-weight: 600; 
    padding: 6px 14px; 
    border-radius: 30px; 
    letter-spacing: 0.5px; 
    text-transform: uppercase; 
    margin: 0 0.4rem 0.4rem 0;
    border: 1px solid rgba(255, 255, 255, 0.3);
}}

.hero-title {{
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0.5rem 0;
    color: white;
    line-height: 1.2;
}}

.hero-description {{
    font-size: 1rem;
    line-height: 1.5;
    color: rgba(255, 255, 255, 0.9);
    margin: 1rem 0;
    max-width: 800px;
}}

.metric-badges {{
    margin-top: 1.2rem;
}}

.metric-badge {{ 
    display: inline-flex; 
    align-items: center; 
    gap: 0.4rem; 
    background: rgba(255,255,255,0.9); 
    padding: 8px 16px; 
    border-radius: 30px; 
    border: 1px solid #dbe4f2; 
    font-size: 0.75rem; 
    font-weight: 500; 
    margin: 6px 10px 0 0; 
    color: #29415a;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}}

/* Enhanced Chat styling */
div[data-testid="stChatMessage"] {{ 
    border-radius: 20px; 
    padding: 1rem 1.5rem; 
    margin-bottom: 1rem; 
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}}

div[data-testid="stChatMessage"] p {{ 
    margin-bottom: 0.5rem; 
    line-height: 1.6;
}}

/* Assistant messages with classic blue styling */
div[data-testid="stChatMessage"][data-testid*="assistant"], 
div[data-testid="stChatMessage"].assistant-msg {{
    background: linear-gradient(145deg, rgba(255,255,255,0.9) 0%, rgba(248,250,255,0.9) 100%); 
    border-left: 4px solid #5b9bd5;
    box-shadow: 0 4px 20px rgba(32,60,120,0.1);
}}

/* User messages with classic blue styling */
div[data-testid="stChatMessage"][data-testid*="user"], 
div[data-testid="stChatMessage"].user-msg {{ 
    background: linear-gradient(145deg, rgba(25,75,251,0.1) 0%, rgba(91,155,213,0.1) 100%); 
    border-left: 4px solid #194bfb;
    box-shadow: 0 4px 20px rgba(25,75,251,0.1);
}}

/* Chat input container */
.stChatFloatingInputContainer {{ 
    border-top: 1px solid rgba(255, 255, 255, 0.2); 
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    border-radius: 20px 20px 0 0;
}}

/* Enhanced scrollbar with classic blue styling */
::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-track {{ background: rgba(255, 255, 255, 0.1); }}
::-webkit-scrollbar-thumb {{ 
    background: linear-gradient(145deg, #5b9bd5, #194bfb); 
    border-radius: 10px; 
}}
::-webkit-scrollbar-thumb:hover {{ background: linear-gradient(145deg, #82a8d6, #5b9bd5); }}

/* Beautiful buttons with dark blue styling */
.stButton > button {{
    background: #003147;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.5rem 1rem;
    font-weight: 500;
    box-shadow: 0 4px 15px rgba(0, 49, 71, 0.3);
    transition: all 0.3s ease;
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 49, 71, 0.4);
    background: #004968;
}}

/* Info boxes enhancement with classic blue styling */
.stInfo {{
    background: linear-gradient(145deg, rgba(25, 75, 251, 0.1) 0%, rgba(255, 255, 255, 0.8) 100%);
    border-left: 4px solid #5b9bd5;
    border-radius: 12px;
    backdrop-filter: blur(10px);
}}

/* Responsive design */
@media (max-width: 768px) {{
    .hero-card {{
        flex-direction: column;
        text-align: center;
        padding: 1.5rem;
    }}
    
    .profile-photo {{
        width: 140px;
        height: 140px;
    }}
    
    .hero-title {{
        font-size: 1.8rem;
    }}
}}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)

_inject_css()

# Simple header with dark blue background
st.markdown("""
<div style='background: #003147; 
            padding: 1rem 2rem; 
            margin: -1rem -1rem 2rem -1rem; 
            border-radius: 0 0 20px 20px;'>
    <h1 style='color: white; margin: 0; font-size: 1.8rem; font-weight: 700; text-align: center;'></h1>
</div>
""", unsafe_allow_html=True)

# Sidebar - moved here so use_uploaded is available
with st.sidebar:
    st.header("🔧 Controls")
    
    # Vector source selection
    st.subheader(" Vector Source")
    use_uploaded = st.radio(
        "Choose content source:",
        options=[False, True],
        format_func=lambda x: " Knowledge Base " if not x else "📄 Uploaded File",
        help="Switch between your base knowledge and uploaded file vectors"
    )
    
    # File upload section
    st.subheader("📁 Upload CV/Resume")
    uploaded_file = st.file_uploader(
        "Choose your CV/Resume file",
        type=["txt", "pdf"],
        help="Upload a TXT or PDF file to add to the knowledge base"
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.type == "application/pdf" or uploaded_file.name.lower().endswith(".pdf"):
                st.info("🔄 Processing PDF...")
                text_content = extract_pdf_text(uploaded_file)
                st.success(f"✅ PDF processed: {uploaded_file.name}")
            else:
                text_content = uploaded_file.read().decode("utf-8", errors="ignore")
                st.success(f"✅ Text file uploaded: {uploaded_file.name}")
            
            if text_content.strip():
                with open("uploaded_content.txt", "w", encoding="utf-8") as f:
                    f.write(text_content)
                st.success("✅ Content saved for processing")
                st.cache_resource.clear()
            else:
                st.error("❌ No readable content found")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    # Current knowledge base info
    st.subheader(" Knowledge Base Status")
    try:
        with open("knowledge_base.txt", "r", encoding="utf-8") as f:
            kb_content = f.read()
        st.info(f" Base: {len(kb_content):,} characters")
        
        if os.path.exists("uploaded_content.txt"):
            with open("uploaded_content.txt", "r", encoding="utf-8") as f:
                uploaded_content = f.read()
            st.info(f"📄 Uploaded: {len(uploaded_content):,} characters")
    except FileNotFoundError:
        st.warning("⚠️ Knowledge base file not found")
    
    # Manual rebuild
    if st.button("🔄 Rebuild Vectors"):
        st.cache_resource.clear()
        st.success("✅ Vectors will rebuild on next query")

# Get profile image as base64 for inline use
banner_b64 = ""
profile_paths = ["phto.jpg", "assets/profile.jpg"]

for profile_path in profile_paths:
    try:
        with open(profile_path, "rb") as f:
            banner_b64 = base64.b64encode(f.read()).decode()
            break
    except Exception:
        continue

# Main Layout - Profile Left, Chat Right
main_col1, main_col2 = st.columns([1, 2])

# Left Column - Profile Section
with main_col1:
    # Inject profile CSS first
    profile_css = """
    <style>
    .profile-container {
        background: #003147;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
    }
    .profile-photo {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        margin: 0 auto 1rem auto;
        background: url(data:image/jpeg;base64,""" + banner_b64 + """) center top 1px/cover no-repeat;
        border: 4px solid rgba(255,255,255,0.8);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    .skill-tag {
        background: rgba(255,255,255,0.2);
        color: white;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 2px;
        display: inline-block;
    }
    </style>
    """
    st.markdown(profile_css, unsafe_allow_html=True)
    
    # Profile content
    st.markdown("""
    <div class='profile-container'>
        <div class='profile-photo'></div>
        <h1 style='font-size: 1.8rem; margin-bottom: 0.5rem; font-weight: 700;'>
            Abdolamir Karbalaie
        </h1>
        <div style='margin-bottom: 1.5rem;'>
            <span class='skill-tag'>AI Engineer</span>
            <span class='skill-tag'>RAG & GenAI</span>
            <span class='skill-tag'>MLOps</span>
            <span class='skill-tag'>LLM Safety</span>
        </div>
        <p style='font-size: 0.9rem; line-height: 1.4; opacity: 0.9;'>
            Senior AI Engineer and Data Scientist specializing in Retrieval Augmented Generation, MLOps, and reliable AI systems development.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional Social Links
    st.markdown("### 🔗 Professional Links")
    st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/abdolamir-karbalaie-3bab9451/)")
    st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/abdkar)")
    st.markdown("[![Google Scholar](https://img.shields.io/badge/Google%20Scholar-4285F4?style=for-the-badge&logo=google-scholar&logoColor=white)](https://scholar.google.com/citations?user=Noi7TFUAAAA)")
    st.markdown("[![Web of Science](https://img.shields.io/badge/Web%20of%20Science-1E88E5?style=for-the-badge&logo=clarivate&logoColor=white)](https://www.webofscience.com/wos/author/record/B-6201-2016)")

# Right Column - Chat Interface
with main_col2:
    st.markdown("#  Chat with my AI Professional Persona")
    st.markdown("*Ask about experience, architecture decisions, measurable impact, leadership, or how I deliver reliable AI systems. Answers are strictly grounded in my curated professional knowledge base (RAG retrieval).*")
    
    # Welcome message

    
    # Quick Start Questions
    st.markdown("###  Quick Start Questions")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🔚 End-to-End ML", use_container_width=True):
            st.session_state.suggested_query = "Tell me about your end-to-end machine learning experience"
    with col2:
        if st.button(" Technical skills", use_container_width=True):
            st.session_state.suggested_query = "Tell me about your Technical skills experience"
    with col3:
        if st.button(" Reliability", use_container_width=True):
            st.session_state.suggested_query = "How do you ensure reliability in AI systems?"
    with col4:
        if st.button(" RAG", use_container_width=True):
            st.session_state.suggested_query = "Tell me about your experience with RAG development and deployment"
    
    # Chat Interface inside right column
    st.markdown("---")
    st.markdown("### 💬 Start Chatting")
    
    # Load RAG pipeline
    kb_hash_now = get_kb_hash()
    rag_bundle = load_rag_pipeline(kb_hash_now, use_uploaded=use_uploaded)

    if rag_bundle is None:
        st.error("❌ Could not load RAG pipeline. Please check your knowledge base file.")
        st.stop()

    qa_chain = rag_bundle["chain"]

    # Handle suggested queries first
    if "suggested_query" in st.session_state:
        user_prompt = st.session_state.suggested_query
        del st.session_state.suggested_query
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        # Generate and add response to chat history
        try:
            response = qa_chain.invoke({"query": user_prompt})
            
            # Handle different response formats from LangChain
            if isinstance(response, dict):
                response = response.get('result', str(response))
            
            if not response or (isinstance(response, str) and response.strip() == ""):
                response = "I apologize, but I couldn't generate a response. This might be due to API limitations. Please try rephrasing your question or try again later."
            
        except Exception as e:
            if "quota" in str(e).lower() or "limit" in str(e).lower():
                response = "⚠️ API quota exceeded. The free tier has daily limits. Please try again later or upgrade your API plan."
            else:
                response = f"❌ Error: {str(e)}"
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Display all chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
            st.markdown(message["content"])

    # Chat input at the bottom
    user_prompt = st.chat_input("Ask about the CV/Resume...")
    
    if user_prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        # Generate and add response to chat history
        try:
            response = qa_chain.invoke({"query": user_prompt})
            
            # Handle different response formats from LangChain
            if isinstance(response, dict):
                response = response.get('result', str(response))
            
            if not response or (isinstance(response, str) and response.strip() == ""):
                response = "I apologize, but I couldn't generate a response. This might be due to API limitations. Please try rephrasing your question or try again later."
            
        except Exception as e:
            if "quota" in str(e).lower() or "limit" in str(e).lower():
                response = "⚠️ API quota exceeded. The free tier has daily limits. Please try again later or upgrade your API plan."
            else:
                response = f"❌ Error: {str(e)}"
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to display the new messages
        st.rerun()
    
    # Footer
    st.caption(f"Vector store built: {rag_bundle.get('built_at','?')} | KB {rag_bundle.get('kb_hash','?')[:12]}…")
