"""
Streamlit Cloud-compatible file processing module.
Handles PDF and text file processing with cloud environment compatibility.
"""

import os
import hashlib
from typing import Optional, Any, Dict
import streamlit as st


def extract_pdf_text_cloud(uploaded_file: Any) -> str:
    """
    Extract text from PDF file using pypdf - Cloud compatible.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Extracted text content
        
    Raises:
        Exception: If PDF processing fails
    """
    try:
        from pypdf import PdfReader
        
        # Reset file pointer to beginning
        uploaded_file.seek(0)
        
        reader = PdfReader(uploaded_file)
        text = ""
        
        if len(reader.pages) == 0:
            raise Exception("PDF file contains no pages")
        
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
        raise Exception(f"PDF processing failed: {str(e)}")


def extract_text_file_cloud(uploaded_file: Any) -> str:
    """
    Extract text from text file - Cloud compatible.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Text content
        
    Raises:
        Exception: If text processing fails
    """
    try:
        # Reset file pointer to beginning
        uploaded_file.seek(0)
        
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                uploaded_file.seek(0)
                content = uploaded_file.read().decode(encoding)
                if content.strip():
                    return content.strip()
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        raise Exception("Could not decode text file with any common encoding")
        
    except Exception as e:
        raise Exception(f"Text file processing failed: {str(e)}")


def validate_name_in_content_cloud(content: str) -> bool:
    """
    Check if the content contains expected name variations - Cloud compatible.
    
    Args:
        content: Text content to validate
        
    Returns:
        True if any name variation is found, False otherwise
    """
    content_lower = content.lower()
    name_variations = [
        "abdolamir karbalaie",
        "abdolamir", 
        "karbalaie",
        "amir karbalaie",
        "amir"
    ]
    return any(name.lower() in content_lower for name in name_variations)


def load_knowledge_base_cloud() -> str:
    """
    Load content from the main knowledge base file - Cloud compatible.
    
    Returns:
        Knowledge base content
        
    Raises:
        FileNotFoundError: If knowledge base file doesn't exist
    """
    try:
        # Try different possible paths
        file_paths = ["knowledge_base.txt", "data/knowledge_base.txt", "./knowledge_base.txt"]
        
        for file_path in file_paths:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
        
        raise FileNotFoundError(f"Knowledge base file not found in any of: {file_paths}")
        
    except Exception as e:
        raise FileNotFoundError(f"Could not load knowledge base: {str(e)}")


def process_uploaded_file_cloud(uploaded_file: Any) -> Optional[str]:
    """
    Process uploaded file for Streamlit Cloud - stores in session state only.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Extracted content if successful, None otherwise
    """
    try:
        # Validate file size (limit to 10MB)
        if uploaded_file.size > 10 * 1024 * 1024:
            st.error("❌ File too large. Maximum size is 10MB.")
            return None
        
        # Extract content based on file type
        content = None
        file_type = uploaded_file.type
        
        if file_type == "application/pdf":
            st.info("📄 Processing PDF file...")
            content = extract_pdf_text_cloud(uploaded_file)
        elif file_type == "text/plain" or uploaded_file.name.endswith('.txt'):
            st.info("📝 Processing text file...")
            content = extract_text_file_cloud(uploaded_file)
        else:
            st.error(f"❌ Unsupported file type: {file_type}")
            st.info("💡 Supported formats: PDF (.pdf), Text (.txt)")
            return None
        
        if not content or not content.strip():
            st.error("❌ No content could be extracted from the file")
            return None
            
        # Basic content validation
        if len(content) < 50:
            st.warning("⚠️ File content seems very short. Make sure it contains your CV/Resume information.")
        
        # Validate name presence
        if not validate_name_in_content_cloud(content):
            st.warning("⚠️ The uploaded content doesn't appear to contain expected name variations.")
            st.info("💡 Make sure this is the correct CV/Resume file.")
        
        # Store in session state instead of file system
        st.session_state.uploaded_content = content
        st.session_state.uploaded_filename = uploaded_file.name
        st.session_state.upload_timestamp = st.session_state.get('upload_timestamp', 0) + 1
        
        # Show success message with file stats
        word_count = len(content.split())
        st.success(f"✅ Successfully processed **{uploaded_file.name}**")
        st.info(f"📊 **{len(content):,}** characters • **{word_count:,}** words extracted")
        
        return content
        
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.info("💡 Try checking that your file is a valid PDF or text file")
        return None


def get_uploaded_content_cloud() -> Optional[str]:
    """
    Get uploaded content from session state - Cloud compatible.
    
    Returns:
        Uploaded content if available, None otherwise
    """
    return st.session_state.get('uploaded_content', None)


def clear_uploaded_content_cloud():
    """
    Clear uploaded content from session state - Cloud compatible.
    """
    for key in ['uploaded_content', 'uploaded_filename', 'upload_timestamp']:
        if key in st.session_state:
            del st.session_state[key]


def get_content_stats_cloud(content: str) -> Dict[str, int]:
    """
    Get statistics about content - Cloud compatible.
    
    Args:
        content: Text content to analyze
        
    Returns:
        Dictionary with content statistics
    """
    return {
        "characters": len(content),
        "words": len(content.split()),
        "lines": len(content.splitlines()),
        "paragraphs": len([p for p in content.split('\n\n') if p.strip()])
    }


def get_content_hash_cloud(content: str) -> str:
    """
    Generate MD5 hash of content for caching purposes - Cloud compatible.
    
    Args:
        content: Content to hash
        
    Returns:
        MD5 hash string
    """
    return hashlib.md5(content.encode()).hexdigest()


def is_cloud_environment() -> bool:
    """
    Detect if running on Streamlit Cloud.
    
    Returns:
        True if running on Streamlit Cloud, False otherwise
    """
    # Check common Streamlit Cloud environment indicators
    cloud_indicators = [
        'STREAMLIT_CLOUD' in os.environ,
        'streamlit.app' in os.environ.get('STREAMLIT_SERVER_HEADLESS', ''),
        '/mount/src' in os.getcwd(),
        'share.streamlit.io' in os.environ.get('STREAMLIT_SERVER_BASE_URL', ''),
        os.environ.get('STREAMLIT_RUNTIME_ENVIRONMENT') == 'cloud'
    ]
    
    return any(cloud_indicators)


# Auto-detect environment and use appropriate functions
def extract_pdf_text(uploaded_file: Any) -> str:
    """Auto-detect environment and use appropriate PDF extraction."""
    if is_cloud_environment():
        return extract_pdf_text_cloud(uploaded_file)
    else:
        # Import and use local version
        from .file_processing import extract_pdf_text as local_extract
        return local_extract(uploaded_file)


def extract_text_file(uploaded_file: Any) -> str:
    """Auto-detect environment and use appropriate text extraction."""
    if is_cloud_environment():
        return extract_text_file_cloud(uploaded_file)
    else:
        # Import and use local version
        from .file_processing import extract_text_file as local_extract
        return local_extract(uploaded_file)


def save_uploaded_content(uploaded_file: Any) -> Optional[str]:
    """Auto-detect environment and use appropriate content saving."""
    if is_cloud_environment():
        return process_uploaded_file_cloud(uploaded_file)
    else:
        # Import and use local version
        from .file_processing import save_uploaded_content as local_save
        return local_save(uploaded_file)


def load_uploaded_content() -> Optional[str]:
    """Auto-detect environment and use appropriate content loading."""
    if is_cloud_environment():
        return get_uploaded_content_cloud()
    else:
        # Import and use local version
        from .file_processing import load_uploaded_content as local_load
        return local_load()


def clear_uploaded_content():
    """Auto-detect environment and use appropriate content clearing."""
    if is_cloud_environment():
        clear_uploaded_content_cloud()
    else:
        # For local, remove the file
        try:
            if os.path.exists("uploaded_content.txt"):
                os.remove("uploaded_content.txt")
            if os.path.exists("data/uploaded_content.txt"):
                os.remove("data/uploaded_content.txt")
        except Exception:
            pass


def load_knowledge_base() -> str:
    """Auto-detect environment and use appropriate knowledge base loading."""
    if is_cloud_environment():
        return load_knowledge_base_cloud()
    else:
        # Import and use local version
        from .file_processing import load_knowledge_base as local_load
        return local_load()
