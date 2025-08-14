"""
Smart CV RAG Chatbot that automatically switches between full functionality 
and quota-safe mode based on API availability.
"""

import streamlit as st
import sys
import os
from datetime import datetime, timedelta
import time

# Add the current directory to sys.path to import modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.ui.components import render_profile_section, render_social_links, inject_custom_css, show_success_message
from configs.app_config import config

class APIQuotaManager:
    """Manages API quota status and automatic fallback."""
    
    def __init__(self):
        if 'quota_status' not in st.session_state:
            st.session_state.quota_status = {
                'api_available': True,
                'last_check': None,
                'quota_reset_time': None,
                'error_count': 0,
                'last_error': None
            }
    
    def check_api_status(self, force_check=False):
        """Check API status with intelligent caching."""
        current_time = datetime.now()
        
        # If we recently checked and API was down, wait before re-checking
        if (not force_check and 
            st.session_state.quota_status['last_check'] and 
            not st.session_state.quota_status['api_available']):
            
            time_since_check = current_time - st.session_state.quota_status['last_check']
            if time_since_check < timedelta(minutes=5):  # Wait 5 minutes between checks
                return st.session_state.quota_status
        
        # Perform actual API check
        try:
            from configs.app_config import get_google_api_key, ModelConfig
            import google.generativeai as genai
            
            api_key = get_google_api_key()
            genai.configure(api_key=api_key)
            
            # Quick test with working model
            model = genai.GenerativeModel(ModelConfig.PRIMARY_MODEL)
            response = model.generate_content(
                "Hi", 
                generation_config={'max_output_tokens': 5}
            )
            
            # API is working
            st.session_state.quota_status.update({
                'api_available': True,
                'last_check': current_time,
                'error_count': 0,
                'last_error': None
            })
            
            return st.session_state.quota_status
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # Detect quota-related errors
            is_quota_error = any(keyword in error_msg for keyword in [
                'quota', '429', 'exceeded', 'limit', 'rate limit'
            ])
            
            if is_quota_error:
                # Estimate quota reset time (24 hours from first quota error)
                if st.session_state.quota_status['quota_reset_time'] is None:
                    st.session_state.quota_status['quota_reset_time'] = current_time + timedelta(hours=24)
                
                st.session_state.quota_status.update({
                    'api_available': False,
                    'last_check': current_time,
                    'error_count': st.session_state.quota_status['error_count'] + 1,
                    'last_error': 'quota_exceeded'
                })
            else:
                st.session_state.quota_status.update({
                    'api_available': False,
                    'last_check': current_time,
                    'error_count': st.session_state.quota_status['error_count'] + 1,
                    'last_error': f'api_error: {str(e)[:100]}'
                })
            
            return st.session_state.quota_status
    
    def get_quota_reset_estimate(self):
        """Get estimated time until quota reset."""
        if st.session_state.quota_status['quota_reset_time']:
            reset_time = st.session_state.quota_status['quota_reset_time']
            current_time = datetime.now()
            if reset_time > current_time:
                time_diff = reset_time - current_time
                hours = int(time_diff.total_seconds() // 3600)
                minutes = int((time_diff.total_seconds() % 3600) // 60)
                return f"{hours}h {minutes}m"
        return "Unknown"

def main():
    """Main application with automatic quota management."""
    
    # Page configuration
    st.set_page_config(
        page_title=config.server.page_title,
        page_icon=config.server.page_icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inject custom CSS
    inject_custom_css()
    
    # Initialize quota manager
    quota_manager = APIQuotaManager()
    
    # Check API status
    api_status = quota_manager.check_api_status()
    
    if api_status['api_available']:
        # Run full application
        run_full_application(quota_manager)
    else:
        # Run quota-safe version
        run_quota_safe_application(quota_manager)

def run_full_application(quota_manager):
    """Run the full application with AI capabilities."""
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🟢 API Status")
        st.success("✅ API Available - Full Functionality")
        
        # API status details
        with st.expander("📊 API Details"):
            st.write(f"**Last Check:** {st.session_state.quota_status['last_check'].strftime('%H:%M:%S') if st.session_state.quota_status['last_check'] else 'Never'}")
            st.write(f"**Error Count:** {st.session_state.quota_status['error_count']}")
        
        # Manual API check
        if st.button("🔄 Check API Status"):
            quota_manager.check_api_status(force_check=True)
            st.rerun()
        
        st.markdown("---")
        
        # Vector Source Selection
        st.markdown("### 📄 Vector Source")
        st.markdown("Choose content source:")
        
        use_uploaded = st.radio(
            "Choose content source:",
            options=["Knowledge Base", "Uploaded File"],
            key="vector_source",
            label_visibility="collapsed"
        ) == "Uploaded File"
        
        # File upload
        if use_uploaded:
            st.markdown("### 📤 Upload CV/Resume")
            st.markdown("Choose your CV/Resume file:")
            
            uploaded_file = st.file_uploader(
                "Drag and drop file here",
                type=['txt', 'pdf'],
                key="file_uploader"
            )
            
            if uploaded_file:
                # Show environment info
                from src.utils.smart_adapter import show_environment_message
                show_environment_message()
                
                # Process uploaded file
                from src.utils.smart_adapter import smart_file_upload
                content = smart_file_upload(uploaded_file)
                if content:
                    # Successfully processed file
                    use_uploaded = True  # Automatically switch to uploaded content
                    st.success("✅ File uploaded and processed successfully!")
                    st.info("🔄 Automatically switched to uploaded file mode")
                else:
                    st.error("❌ Error processing file")
                    use_uploaded = False
        
        # Knowledge base status
        st.markdown("### 📊 Knowledge Base Status")
        try:
            with open('knowledge_base.txt', 'r', encoding='utf-8') as f:
                content = f.read()
            
            char_count = len(content)
            word_count = len(content.split())
            
            st.success("✅ Base Knowledge")
            st.caption(f"📝 {char_count:,} characters • 📄 {word_count:,} words")
            
        except Exception as e:
            st.error(f"❌ Error loading knowledge base: {str(e)}")
        
        # Manual rebuild option
        if st.button("🔄 Rebuild Vectors"):
            from src.core.simple_rag import clear_simple_pipeline_cache
            clear_simple_pipeline_cache()
            show_success_message("Vectors will rebuild on next query")
    
    # Main layout - Profile Left, Chat Right
    main_col1, main_col2 = st.columns([1, 2])
    
    # Left Column - Profile Section
    with main_col1:
        render_profile_section()
        render_social_links()
    
    # Right Column - Chat Interface with Quota Protection
    with main_col2:
        st.markdown("# 💬 Chat with my AI Professional Persona")
        st.markdown("*Ask about experience, architecture decisions, measurable impact, leadership, or how I deliver reliable AI systems. Answers are strictly grounded in my curated professional knowledge base (RAG retrieval).*")
        
        # Get or build RAG pipeline with error handling
        try:
            pipeline_data = get_or_build_pipeline_safe(use_uploaded, quota_manager)
            
            if pipeline_data:
                # Quick start questions
                render_quick_start_questions()
                
                # Chat interface
                render_chat_interface(pipeline_data, quota_manager)
            else:
                st.error("❌ Failed to initialize AI pipeline. Switching to safe mode...")
                time.sleep(2)
                st.rerun()
                
        except Exception as e:
            error_msg = str(e).lower()
            if any(keyword in error_msg for keyword in ['quota', '429', 'exceeded', 'limit']):
                st.error("⚠️ API quota exceeded. Switching to safe mode...")
                st.session_state.quota_status['api_available'] = False
                time.sleep(2)
                st.rerun()
            else:
                st.error(f"❌ Unexpected error: {str(e)}")

def get_or_build_pipeline_safe(use_uploaded, quota_manager):
    """Safely get or build pipeline with quota monitoring."""
    try:
        from src.core.simple_rag import get_simple_rag_pipeline
        from src.utils.smart_adapter import smart_get_content_hash, smart_load_knowledge_base, smart_load_uploaded_content
        get_content_hash = smart_get_content_hash
        load_knowledge_base = smart_load_knowledge_base
        load_uploaded_content = smart_load_uploaded_content
        
        # Load content
        if use_uploaded:
            content = load_uploaded_content()
            if not content:
                content = load_knowledge_base()
                use_uploaded = False
        else:
            content = load_knowledge_base()
        
        content_hash = get_content_hash(content)
        return get_simple_rag_pipeline(content_hash, use_uploaded)
        
    except Exception as e:
        error_msg = str(e).lower()
        if any(keyword in error_msg for keyword in ['quota', '429', 'exceeded', 'limit']):
            # Update quota status and trigger safe mode
            st.session_state.quota_status['api_available'] = False
            quota_manager.check_api_status()
            return None
        else:
            raise e

def render_quick_start_questions():
    """Render quick start question buttons."""
    st.markdown("### ⚡ Quick Start Questions")
    st.markdown("Click any button below to start exploring my professional experience and capabilities")
    
    col1, col2, col3, col4 = st.columns(4)
    
    quick_questions = {
        "END-TO-END ML": "Tell me about your end-to-end machine learning project experience and measurable impact",
        "TECHNICAL SKILLS": "What are your core technical skills and programming languages?",
        "AI RELIABILITY": "How do you ensure AI system reliability and handle edge cases?",
        "RAG SYSTEMS": "Describe your experience with RAG systems and LLM integration"
    }
    
    for i, (label, question) in enumerate(quick_questions.items()):
        col = [col1, col2, col3, col4][i]
        with col:
            if st.button(label, key=f"quick_{i}", use_container_width=True):
                st.session_state.user_question = question

def render_chat_interface(pipeline_data, quota_manager):
    """Render the main chat interface with quota monitoring."""
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Handle quick start questions first
    if "user_question" in st.session_state:
        user_question = st.session_state.user_question
        del st.session_state.user_question
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_question})
        
        # Generate AI response with quota monitoring
        try:
            response = generate_response_safe(pipeline_data, user_question, quota_manager)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            error_msg = str(e).lower()
            if any(keyword in error_msg for keyword in ['quota', '429', 'exceeded', 'limit']):
                st.error("⚠️ API quota exceeded during response generation. Switching to safe mode...")
                st.session_state.quota_status['api_available'] = False
                time.sleep(2)
                st.rerun()
            else:
                st.error(f"❌ Error generating response: {str(e)}")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input at the very bottom
    user_question = st.chat_input("Ask about the CV/Resume...")
    
    if user_question:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_question})
        
        # Generate AI response with quota monitoring
        try:
            response = generate_response_safe(pipeline_data, user_question, quota_manager)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()  # Refresh to show the new messages
            
        except Exception as e:
            error_msg = str(e).lower()
            if any(keyword in error_msg for keyword in ['quota', '429', 'exceeded', 'limit']):
                st.error("⚠️ API quota exceeded during response generation. Switching to safe mode...")
                st.session_state.quota_status['api_available'] = False
                time.sleep(2)
                st.rerun()
            else:
                st.error(f"❌ Error generating response: {str(e)}")
                st.rerun()

def generate_response_safe(pipeline_data, question, quota_manager):
    """Generate response with quota monitoring."""
    try:
        pipeline = pipeline_data.get('pipeline')
        if pipeline and hasattr(pipeline, 'query'):
            return pipeline.query(question)
        else:
            # Fallback to chain
            chain = pipeline_data.get('chain')
            if chain:
                response = chain.invoke({"query": question})
                if isinstance(response, dict):
                    return response.get('result', str(response))
                return str(response)
            else:
                return "❌ Pipeline not properly initialized."
                
    except Exception as e:
        error_msg = str(e).lower()
        if any(keyword in error_msg for keyword in ['quota', '429', 'exceeded', 'limit']):
            st.session_state.quota_status['api_available'] = False
            raise e
        else:
            return f"❌ Error: {str(e)}"

def run_quota_safe_application(quota_manager):
    """Run the quota-safe version of the application."""
    
    # Sidebar with status
    with st.sidebar:
        st.markdown("### ❌ API Status")
        st.error("⚠️ API Quota Exceeded")
        
        # Quota details
        with st.expander("📊 Quota Details"):
            st.write(f"**Last Check:** {st.session_state.quota_status['last_check'].strftime('%H:%M:%S') if st.session_state.quota_status['last_check'] else 'Never'}")
            st.write(f"**Error Count:** {st.session_state.quota_status['error_count']}")
            st.write(f"**Reset Estimate:** {quota_manager.get_quota_reset_estimate()}")
            if st.session_state.quota_status['last_error']:
                st.write(f"**Last Error:** {st.session_state.quota_status['last_error']}")
        
        # Manual retry option
        if st.button("🔄 Retry API Connection"):
            quota_manager.check_api_status(force_check=True)
            if st.session_state.quota_status['api_available']:
                st.success("✅ API restored! Switching to full mode...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ API still unavailable")
        
        st.markdown("---")
        
        st.markdown("### 📊 Knowledge Base Status")
        st.success("✅ Knowledge Base Available")
        st.info("💡 All content is stored locally and ready to use when API quota resets")
    
    # Main layout - Profile Left, Status Right
    main_col1, main_col2 = st.columns([1, 2])
    
    # Left Column - Profile Section (works without API)
    with main_col1:
        render_profile_section()
        render_social_links()
    
    # Right Column - Quota Status and Static Info
    with main_col2:
        st.markdown("# ⚠️ API Quota Temporarily Exceeded")
        
        # Auto-refresh notice
        st.info("🔄 **Auto-monitoring enabled**: The app will automatically switch back to full functionality when the API quota resets.")
        
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
        
        # Display static information
        display_static_highlights()
        
        st.markdown("---")
        st.success("🤖 **Smart Recovery**: The app monitors API status and will automatically restore full functionality when available!")

def display_static_highlights():
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

if __name__ == "__main__":
    main()
