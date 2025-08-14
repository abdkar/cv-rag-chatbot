"""
Quota-safe version of the CV RAG Chatbot that handles API limits gracefully.
"""

import streamlit as st
import sys
import os

# Add the current directory to sys.path to import modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.ui.components import render_profile_section, render_social_links, inject_custom_css
from configs.app_config import config

def main():
    """Main application function with quota-safe error handling."""
    
    # Page configuration
    st.set_page_config(
        page_title=config.server.page_title,
        page_icon=config.server.page_icon,
        layout=config.server.layout,
        initial_sidebar_state=config.server.initial_sidebar_state
    )
    
    # Inject custom CSS
    inject_custom_css()
    
    # Check if we can connect to the API
    api_status = check_api_status()
    
    if not api_status['available']:
        display_quota_exceeded_page(api_status['error'])
        return
    
    # If API is available, run normal app
    run_normal_app()

def check_api_status():
    """Check if the Google Gemini API is available."""
    try:
        from configs.app_config import get_google_api_key
        import google.generativeai as genai
        
        api_key = get_google_api_key()
        genai.configure(api_key=api_key)
        
        # Try a minimal test
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hello", generation_config={'max_output_tokens': 10})
        
        return {'available': True, 'error': None}
        
    except Exception as e:
        error_msg = str(e)
        if "quota" in error_msg.lower() or "429" in error_msg or "exceeded" in error_msg.lower():
            return {'available': False, 'error': 'quota_exceeded'}
        else:
            return {'available': False, 'error': f'api_error: {error_msg}'}

def display_quota_exceeded_page(error_type):
    """Display a user-friendly quota exceeded page."""
    
    # Sidebar with basic info
    with st.sidebar:
        st.markdown("### 🔄 API Status")
        st.error("❌ API Quota Exceeded")
        st.markdown("### 📊 Knowledge Base Status")
        st.success("✅ Knowledge Base Available")
        st.info("💡 All content is stored locally and ready to use when API quota resets")
    
    # Main layout - Profile Left, Status Right
    main_col1, main_col2 = st.columns([1, 2])
    
    # Left Column - Profile Section (works without API)
    with main_col1:
        render_profile_section()
        render_social_links()
    
    # Right Column - Quota Status
    with main_col2:
        st.markdown("# ⚠️ API Quota Temporarily Exceeded")
        
        st.markdown("""
        ### 🔄 What's happening?
        The Google Gemini API has reached its usage quota. This is a temporary limitation.
        
        ### ⏰ When will it be back?
        - **Free Tier**: Quotas typically reset every 24 hours
        - **Paid Tier**: Usually resolves within an hour
        
        ### 💡 What you can see right now:
        ✅ **Professional Profile** - Complete CV and experience overview  
        ✅ **Visual Design** - Beautiful, professional interface  
        ✅ **Social Links** - Direct access to LinkedIn, GitHub, and publications  
        ✅ **Knowledge Base** - All content is stored and ready  
        
        ### 🚀 What will work when quota resets:
        🤖 **AI Chat** - Interactive Q&A about experience and projects  
        📊 **Smart Retrieval** - Semantic search through professional history  
        🔍 **Deep Insights** - AI-powered analysis of skills and achievements  
        """)
        
        st.markdown("---")
        
        # Display static information that doesn't require API
        display_static_info()
        
        st.markdown("---")
        st.info("💡 **Tip**: Bookmark this page and return in a few hours when the API quota resets!")

def display_static_info():
    """Display key information without requiring API calls."""
    
    st.markdown("### 🎯 Key Highlights (Available Now)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🏆 Recent Achievements:**
        - Research Highlight in Nature Climate Change (2024)
        - Best Poster Award Nominee (2024)
        - 100K SEK Research Grant Awarded (2025)
        
        **💼 Current Role:**
        - Staff Scientist at Umeå University
        - Machine Learning & AI Systems Development
        - Biomechanical Data Analysis
        """)
    
    with col2:
        st.markdown("""
        **🔬 Research Areas:**
        - Medical AI & Computer Vision
        - RAG Systems & LLM Integration
        - Sports Rehabilitation Technology
        - Explainable AI (XAI)
        
        **📊 Publications:**
        - 20+ Journal Papers
        - 15+ Conference Presentations
        - 50+ Citations on Google Scholar
        """)

def run_normal_app():
    """Run the normal application when API is available."""
    st.success("🟢 API Available - Full functionality enabled!")
    st.markdown("*Redirecting to full application...*")
    st.rerun()

if __name__ == "__main__":
    main()
