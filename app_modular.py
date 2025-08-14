"""
Main application module for CV RAG Chatbot.
Professional, modular implementation with clean separation of concerns.
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our modular components
from config import config
from file_processing import (
    extract_pdf_text, 
    save_uploaded_content, 
    get_knowledge_base_hash,
    validate_name_in_content
)
from rag_pipeline import get_rag_pipeline, clear_pipeline_cache
from ui_components import (
    inject_custom_css,
    render_profile_section,
    render_social_links,
    render_quick_start_buttons,
    render_sidebar_controls,
    render_knowledge_base_status,
    show_success_message,
    show_error_message,
    show_warning_message
)


class CVChatbotApp:
    """Main application class for the CV RAG Chatbot."""
    
    def __init__(self):
        """Initialize the application."""
        self.setup_page_config()
        self.initialize_session_state()
    
    def setup_page_config(self):
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title=config.server.page_title,
            page_icon=config.server.page_icon,
            layout=config.server.layout,
            initial_sidebar_state=config.server.initial_sidebar_state
        )
    
    def initialize_session_state(self):
        """Initialize session state variables."""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "rag_pipeline" not in st.session_state:
            st.session_state.rag_pipeline = None
    
    def handle_file_upload(self, uploaded_file) -> bool:
        """
        Handle file upload and processing.
        
        Args:
            uploaded_file: Uploaded file object
            
        Returns:
            True if processing successful, False otherwise
        """
        if uploaded_file is None:
            return False
        
        try:
            # Process based on file type
            if uploaded_file.type == "application/pdf" or uploaded_file.name.lower().endswith(".pdf"):
                st.info("🔄 Processing PDF...")
                text_content = extract_pdf_text(uploaded_file)
                show_success_message(f"PDF processed: {uploaded_file.name}")
            else:
                text_content = uploaded_file.read().decode("utf-8", errors="ignore")
                show_success_message(f"Text file uploaded: {uploaded_file.name}")
            
            # Validate and save content
            if text_content.strip():
                if validate_name_in_content(text_content):
                    if save_uploaded_content(text_content):
                        show_success_message("Content saved for processing")
                        clear_pipeline_cache()  # Clear cache to rebuild with new content
                        return True
                    else:
                        show_error_message("Failed to save content")
                else:
                    show_warning_message("Content doesn't contain expected name variations")
            else:
                show_error_message("No readable content found")
                
        except Exception as e:
            show_error_message(f"Error processing file: {str(e)}")
        
        return False
    
    def get_or_build_pipeline(self, use_uploaded: bool):
        """
        Get or build the RAG pipeline.
        
        Args:
            use_uploaded: Whether to use uploaded content
            
        Returns:
            RAG pipeline dictionary or None
        """
        # Get content hash for caching
        kb_hash = get_knowledge_base_hash()
        
        # Get cached pipeline
        pipeline_data = get_rag_pipeline(kb_hash, use_uploaded=use_uploaded)
        
        if pipeline_data is None:
            show_error_message("Could not load RAG pipeline. Please check your knowledge base file.")
            return None
        
        return pipeline_data
    
    def handle_chat_interaction(self, pipeline_data):
        """
        Handle chat interactions and message processing.
        
        Args:
            pipeline_data: RAG pipeline data dictionary
        """
        # Handle suggested queries from quick start buttons
        suggested_query = render_quick_start_buttons()
        if suggested_query:
            self.process_user_message(suggested_query, pipeline_data)
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
                st.markdown(message["content"])
        
        # Handle chat input
        user_prompt = st.chat_input("Ask about the CV/Resume...")
        if user_prompt:
            self.process_user_message(user_prompt, pipeline_data)
            st.rerun()
    
    def process_user_message(self, user_prompt: str, pipeline_data):
        """
        Process user message and generate response.
        
        Args:
            user_prompt: User's input message
            pipeline_data: RAG pipeline data dictionary
        """
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        # Generate response using the pipeline
        try:
            pipeline = pipeline_data.get("pipeline")
            if pipeline:
                response = pipeline.query(user_prompt)
            else:
                response = "❌ Pipeline not available. Please rebuild the system."
        except Exception as e:
            response = f"❌ Error generating response: {str(e)}"
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    def render_main_interface(self):
        """Render the main application interface."""
        # Inject custom CSS
        inject_custom_css()
        
        # Render sidebar controls
        use_uploaded, uploaded_file = render_sidebar_controls()
        
        # Handle file upload
        if uploaded_file:
            self.handle_file_upload(uploaded_file)
        
        # Render knowledge base status in sidebar
        with st.sidebar:
            render_knowledge_base_status()
            
            # Manual rebuild option
            if st.button("🔄 Rebuild Vectors"):
                clear_pipeline_cache()
                show_success_message("Vectors will rebuild on next query")
        
        # Main layout - Profile Left, Chat Right
        main_col1, main_col2 = st.columns([1, 2])
        
        # Left Column - Profile Section
        with main_col1:
            render_profile_section()
            render_social_links()
        
        # Right Column - Chat Interface
        with main_col2:
            st.markdown("# 💬 Chat with my AI Professional Persona")
            st.markdown("*Ask about experience, architecture decisions, measurable impact, leadership, or how I deliver reliable AI systems. Answers are strictly grounded in my curated professional knowledge base (RAG retrieval).*")
            
            # Get or build RAG pipeline
            pipeline_data = self.get_or_build_pipeline(use_uploaded)
            
            if pipeline_data:
                st.markdown("---")
                st.markdown("### 💭 Start Chatting")
                
                # Handle chat interactions
                self.handle_chat_interaction(pipeline_data)
                
                # Footer with build info
                st.caption(f"Vector store built: {pipeline_data.get('built_at', '?')} | "
                         f"KB {pipeline_data.get('content_hash', '?')[:12]}… | "
                         f"Length: {pipeline_data.get('content_length', '?'):,} chars")
    
    def run(self):
        """Run the main application."""
        try:
            self.render_main_interface()
        except Exception as e:
            st.error(f"❌ Application error: {str(e)}")
            st.error("Please check your configuration and try again.")


def main():
    """Main entry point for the application."""
    app = CVChatbotApp()
    app.run()


if __name__ == "__main__":
    main()
