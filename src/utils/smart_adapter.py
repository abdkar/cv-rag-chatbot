"""
Environment detection and automatic switching for file processing.
Detects if running locally or on Streamlit Cloud and uses appropriate methods.
"""

import os
import streamlit as st
from typing import Optional, Any, Dict


def is_streamlit_cloud() -> bool:
    """
    Detect if running on Streamlit Cloud.
    
    Returns:
        True if running on Streamlit Cloud, False otherwise
    """
    # Multiple detection methods for reliability
    cloud_indicators = [
        # Environment variables set by Streamlit Cloud
        'STREAMLIT_CLOUD' in os.environ,
        'GITHUB_REPOSITORY' in os.environ and 'STREAMLIT' in os.environ.get('STREAMLIT_RUNTIME_ENVIRONMENT', ''),
        
        # URL-based detection
        'streamlit.app' in os.environ.get('STREAMLIT_SERVER_BASE_URL', ''),
        'share.streamlit.io' in os.environ.get('STREAMLIT_SERVER_BASE_URL', ''),
        
        # File system indicators
        '/mount/src' in os.getcwd(),
        '/app' in os.getcwd() and not os.path.exists('/home'),
        
        # Runtime environment
        os.environ.get('STREAMLIT_RUNTIME_ENVIRONMENT') == 'cloud'
    ]
    
    return any(cloud_indicators)


def smart_file_upload(uploaded_file: Any) -> Optional[str]:
    """
    Smart file upload that works both locally and on Streamlit Cloud.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Extracted content if successful, None otherwise
    """
    try:
        if is_streamlit_cloud():
            st.info("🌐 Running on Streamlit Cloud - using cloud-optimized processing")
            from src.utils.file_processing_cloud import process_uploaded_file_cloud
            return process_uploaded_file_cloud(uploaded_file)
        else:
            st.info("💻 Running locally - using full file system processing")
            from src.utils.file_processing import save_uploaded_content
            return save_uploaded_content(uploaded_file)
    except Exception as e:
        st.error(f"❌ File processing error: {str(e)}")
        # Fallback to cloud method if local fails
        if not is_streamlit_cloud():
            try:
                st.info("🔄 Trying cloud-compatible method as fallback...")
                from src.utils.file_processing_cloud import process_uploaded_file_cloud
                return process_uploaded_file_cloud(uploaded_file)
            except Exception as fallback_e:
                st.error(f"❌ Fallback also failed: {str(fallback_e)}")
        return None


def smart_load_uploaded_content() -> Optional[str]:
    """
    Smart content loading that works both locally and on Streamlit Cloud.
    
    Returns:
        Uploaded content if available, None otherwise
    """
    try:
        if is_streamlit_cloud():
            # Use session state
            return st.session_state.get('uploaded_content', None)
        else:
            # Use file system
            from src.utils.file_processing import load_uploaded_content
            return load_uploaded_content()
    except Exception:
        # Fallback to session state
        return st.session_state.get('uploaded_content', None)


def smart_clear_uploaded_content():
    """
    Smart content clearing that works both locally and on Streamlit Cloud.
    """
    # Always clear session state
    for key in ['uploaded_content', 'uploaded_filename', 'upload_timestamp']:
        if key in st.session_state:
            del st.session_state[key]
    
    # Also try to clear file system if local
    if not is_streamlit_cloud():
        try:
            from src.utils.file_processing import load_uploaded_content
            # Try to remove files
            for path in ["uploaded_content.txt", "data/uploaded_content.txt"]:
                if os.path.exists(path):
                    os.remove(path)
        except Exception:
            pass  # Ignore file removal errors


def smart_load_knowledge_base() -> str:
    """
    Smart knowledge base loading that works both locally and on Streamlit Cloud.
    
    Returns:
        Knowledge base content
        
    Raises:
        FileNotFoundError: If knowledge base file doesn't exist
    """
    try:
        if is_streamlit_cloud():
            from src.utils.file_processing_cloud import load_knowledge_base_cloud
            return load_knowledge_base_cloud()
        else:
            from src.utils.file_processing import load_knowledge_base
            return load_knowledge_base()
    except Exception as e:
        # Fallback to simple file reading
        try:
            file_paths = ["knowledge_base.txt", "data/knowledge_base.txt", "./knowledge_base.txt"]
            for file_path in file_paths:
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        return f.read()
            raise FileNotFoundError(f"Knowledge base file not found in any of: {file_paths}")
        except Exception as fallback_e:
            raise FileNotFoundError(f"Could not load knowledge base: {str(fallback_e)}")


def smart_get_content_hash(content: str) -> str:
    """
    Smart content hash generation that works both locally and on Streamlit Cloud.
    
    Args:
        content: Content to hash
        
    Returns:
        MD5 hash string
    """
    import hashlib
    return hashlib.md5(content.encode()).hexdigest()


def get_environment_info() -> Dict[str, Any]:
    """
    Get information about the current environment.
    
    Returns:
        Dictionary with environment information
    """
    info = {
        'is_cloud': is_streamlit_cloud(),
        'platform': 'Streamlit Cloud' if is_streamlit_cloud() else 'Local',
        'working_directory': os.getcwd(),
        'python_path': os.environ.get('PYTHONPATH', 'Not set'),
        'file_system_writable': os.access('.', os.W_OK),
    }
    
    # Add cloud-specific info
    if is_streamlit_cloud():
        info.update({
            'github_repo': os.environ.get('GITHUB_REPOSITORY', 'Not available'),
            'streamlit_base_url': os.environ.get('STREAMLIT_SERVER_BASE_URL', 'Not available'),
        })
    
    return info


def display_environment_debug():
    """Display environment debugging information."""
    if st.checkbox("🔧 Show Environment Debug Info", value=False):
        env_info = get_environment_info()
        st.json(env_info)
        
        st.subheader("Session State Keys")
        st.write(list(st.session_state.keys()))
        
        if 'uploaded_content' in st.session_state:
            content = st.session_state['uploaded_content']
            st.write(f"Uploaded content length: {len(content)} characters")


# Environment warning for users
def show_environment_message():
    """Show environment-specific message to users."""
    if is_streamlit_cloud():
        st.info("🌐 **Cloud Mode**: Files are processed in memory for security. Your data stays private and is not saved to disk.")
    else:
        st.info("💻 **Local Mode**: Files are processed and temporarily saved to your local system.")
