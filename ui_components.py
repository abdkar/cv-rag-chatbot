"""
UI Components module for CV RAG Chatbot.
Contains all UI-related functions and styling.
"""

import base64
import streamlit as st
from typing import Optional
from config import config


def load_profile_image() -> str:
    """
    Load profile image and convert to base64.
    
    Returns:
        Base64 encoded image string
    """
    profile_paths = config.ui.profile_photo_paths or []
    for profile_path in profile_paths:
        try:
            with open(profile_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except Exception:
            continue
    return ""


def inject_custom_css():
    """Inject custom CSS styling for the application."""
    
    banner_b64 = load_profile_image()
    
    css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"]  {{ font-family: 'Inter', sans-serif; }}
.block-container {{ max-width: 1400px !important; padding-top: 1rem !important; padding-bottom: 2rem !important; }}

/* Background and main container */
body {{ 
    background: linear-gradient(120deg, #f5f9ff 0%, #eef3fa 55%, #e6edf5 100%); 
}}

.main .block-container {{
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 1.5rem;
    margin-top: 0.5rem;
    box-shadow: 0 8px 24px -6px rgba(32,60,120,0.25), 0 4px 12px rgba(32,60,120,0.12);
    border: 1px solid #d4e0ef;
}}

/* Hide footer but show deploy button */
footer {{ visibility: hidden !important; }}

/* Profile container styling */
.profile-container {{
    background: #003147;
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 1rem;
}}

.profile-photo {{
    width: 150px;
    height: 150px;
    border-radius: 50%;
    margin: 0 auto 1rem auto;
    background: url(data:image/jpeg;base64,{banner_b64}) center top 1px/cover no-repeat;
    border: 4px solid rgba(255,255,255,0.8);
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}}

.skill-tag {{
    background: rgba(255,255,255,0.2);
    color: white;
    padding: 4px 12px;
    border-radius: 15px;
    font-size: 0.8rem;
    margin: 2px;
    display: inline-block;
}}

/* Chat message styling */
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

/* Assistant messages */
div[data-testid="stChatMessage"][data-testid*="assistant"], 
div[data-testid="stChatMessage"].assistant-msg {{
    background: linear-gradient(145deg, rgba(255,255,255,0.9) 0%, rgba(248,250,255,0.9) 100%); 
    border-left: 4px solid #5b9bd5;
    box-shadow: 0 4px 20px rgba(32,60,120,0.1);
}}

/* User messages */
div[data-testid="stChatMessage"][data-testid*="user"], 
div[data-testid="stChatMessage"].user-msg {{ 
    background: linear-gradient(145deg, rgba(25,75,251,0.1) 0%, rgba(91,155,213,0.1) 100%); 
    border-left: 4px solid #194bfb;
    box-shadow: 0 4px 20px rgba(25,75,251,0.1);
}}

/* Enhanced buttons */
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

/* Scrollbar styling */
::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-track {{ background: rgba(255, 255, 255, 0.1); }}
::-webkit-scrollbar-thumb {{ 
    background: linear-gradient(145deg, #5b9bd5, #194bfb); 
    border-radius: 10px; 
}}
::-webkit-scrollbar-thumb:hover {{ background: linear-gradient(145deg, #82a8d6, #5b9bd5); }}

/* Info boxes */
.stInfo {{
    background: linear-gradient(145deg, rgba(25, 75, 251, 0.1) 0%, rgba(255, 255, 255, 0.8) 100%);
    border-left: 4px solid #5b9bd5;
    border-radius: 12px;
    backdrop-filter: blur(10px);
}}

/* Responsive design */
@media (max-width: 768px) {{
    .profile-container {{
        padding: 1.5rem;
    }}
    
    .profile-photo {{
        width: 120px;
        height: 120px;
    }}
}}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)


def render_profile_section():
    """Render the profile section with photo and information."""
    st.markdown(f"""
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


def render_social_links():
    """Render professional social media links."""
    st.markdown("### 🔗 Professional Links")
    
    social_links = config.ui.social_links
    if social_links:
        for platform, url in social_links.items():
            if platform == "LinkedIn":
                st.markdown(f"[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)]({url})")
            elif platform == "GitHub":
                st.markdown(f"[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)]({url})")
            elif platform == "Google Scholar":
                st.markdown(f"[![Google Scholar](https://img.shields.io/badge/Google%20Scholar-4285F4?style=for-the-badge&logo=google-scholar&logoColor=white)]({url})")
            elif platform == "Web of Science":
                st.markdown(f"[![Web of Science](https://img.shields.io/badge/Web%20of%20Science-1E88E5?style=for-the-badge&logo=clarivate&logoColor=white)]({url})")


def render_quick_start_buttons() -> Optional[str]:
    """
    Render quick start question buttons.
    
    Returns:
        Selected question text or None
    """
    st.markdown("### ⚡ Quick Start Questions")
    col1, col2, col3, col4 = st.columns(4)
    
    suggested_query = None
    
    with col1:
        if st.button("🔚 End-to-End ML", use_container_width=True):
            suggested_query = "Tell me about your end-to-end machine learning experience"
    
    with col2:
        if st.button("🔧 Technical skills", use_container_width=True):
            suggested_query = "Tell me about your Technical skills experience"
    
    with col3:
        if st.button("🛡️ Reliability", use_container_width=True):
            suggested_query = "How do you ensure reliability in AI systems?"
    
    with col4:
        if st.button("📚 RAG", use_container_width=True):
            suggested_query = "Tell me about your experience with RAG development and deployment"
    
    return suggested_query


def render_sidebar_controls():
    """
    Render sidebar controls for file upload and settings.
    
    Returns:
        Tuple of (use_uploaded, uploaded_file)
    """
    with st.sidebar:
        st.header("🔧 Controls")
        
        # Vector source selection
        st.subheader("📊 Vector Source")
        use_uploaded = st.radio(
            "Choose content source:",
            options=[False, True],
            format_func=lambda x: "📄 Knowledge Base" if not x else "📤 Uploaded File",
            help="Switch between your base knowledge and uploaded file vectors"
        )
        
        # File upload section
        st.subheader("📁 Upload CV/Resume")
        uploaded_file = st.file_uploader(
            "Choose your CV/Resume file",
            type=["txt", "pdf"],
            help="Upload a TXT or PDF file to add to the knowledge base"
        )
        
        return use_uploaded, uploaded_file


def render_knowledge_base_status():
    """Render current knowledge base status information."""
    import os
    from file_processing import get_content_stats
    
    st.subheader("📊 Knowledge Base Status")
    
    try:
        # Base knowledge base info
        with open(config.knowledge_base_file, "r", encoding="utf-8") as f:
            kb_content = f.read()
        stats = get_content_stats(kb_content)
        st.info(f"📄 Base: {stats['characters']:,} characters, {stats['words']:,} words")
        
        # Uploaded content info
        if os.path.exists(config.uploaded_content_file):
            with open(config.uploaded_content_file, "r", encoding="utf-8") as f:
                uploaded_content = f.read()
            stats = get_content_stats(uploaded_content)
            st.info(f"📤 Uploaded: {stats['characters']:,} characters, {stats['words']:,} words")
            
    except FileNotFoundError:
        st.warning("⚠️ Knowledge base file not found")


def show_success_message(message: str):
    """Show a success message."""
    st.success(f"✅ {message}")


def show_error_message(message: str):
    """Show an error message."""
    st.error(f"❌ {message}")


def show_warning_message(message: str):
    """Show a warning message."""
    st.warning(f"⚠️ {message}")


def show_info_message(message: str):
    """Show an info message."""
    st.info(f"ℹ️ {message}")
