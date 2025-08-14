"""
File processing module for CV RAG Chatbot.
Handles PDF and text file processing, content validation.
"""

import os
import hashlib
from typing import Optional, Any
from config import config
import streamlit as st


def extract_pdf_text(uploaded_file: Any) -> str:
    """
    Extract text from PDF file using pypdf.
    
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


def validate_name_in_content(content: str) -> bool:
    """
    Check if the content contains the expected name variations.
    
    Args:
        content: Text content to validate
        
    Returns:
        True if any name variation is found, False otherwise
    """
    content_lower = content.lower()
    name_variations = config.name_variations or []
    return any(name.lower() in content_lower for name in name_variations)


def load_knowledge_base() -> str:
    """
    Load content from the main knowledge base file.
    
    Returns:
        Knowledge base content
        
    Raises:
        FileNotFoundError: If knowledge base file doesn't exist
    """
    try:
        with open(config.knowledge_base_file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Knowledge base file '{config.knowledge_base_file}' not found")


def load_uploaded_content() -> Optional[str]:
    """
    Load content from uploaded file if it exists and is valid.
    
    Returns:
        Uploaded content if valid, None otherwise
    """
    if not os.path.exists(config.uploaded_content_file):
        return None
    
    try:
        with open(config.uploaded_content_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        if validate_name_in_content(content):
            return content
        else:
            st.warning("⚠️ Uploaded content doesn't contain the expected name. Using knowledge base instead.")
            return None
    except Exception as e:
        st.error(f"Error reading uploaded content: {str(e)}")
        return None


def save_uploaded_content(content: str) -> bool:
    """
    Save uploaded content to file.
    
    Args:
        content: Content to save
        
    Returns:
        True if saved successfully, False otherwise
    """
    try:
        with open(config.uploaded_content_file, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        st.error(f"Error saving uploaded content: {str(e)}")
        return False


def get_content_hash(content: str) -> str:
    """
    Generate MD5 hash of content for caching purposes.
    
    Args:
        content: Content to hash
        
    Returns:
        MD5 hash string
    """
    return hashlib.md5(content.encode()).hexdigest()


def get_knowledge_base_hash() -> str:
    """
    Get hash of current knowledge base for caching.
    
    Returns:
        Hash of knowledge base content or "no_file" if not found
    """
    try:
        content = load_knowledge_base()
        return get_content_hash(content)
    except FileNotFoundError:
        return "no_file"


def get_content_stats(content: str) -> dict[str, int]:
    """
    Get statistics about content.
    
    Args:
        content: Text content to analyze
        
    Returns:
        Dictionary with content statistics
    """
    return {
        "characters": len(content),
        "words": len(content.split()),
        "lines": len(content.splitlines())
    }
