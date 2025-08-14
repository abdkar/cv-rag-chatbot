"""
Configuration module for CV RAG Chatbot.
Contains all configuration constants and settings.
"""

import os
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class ModelConfig:
    """Configuration for AI models and embeddings."""
    model_name: str = "gemini-2.0-flash-exp"
    temperature: float = 0.3
    timeout: int = 15
    embedding_dimension: int = 384

@dataclass
class VectorStoreConfig:
    """Configuration for vector store and text processing."""
    chunk_size: int = 1000
    chunk_overlap: int = 200
    search_k: int = 3

@dataclass
class ServerConfig:
    """Configuration for Streamlit server."""
    page_title: str = "CV Chatbot"
    page_icon: str = "💼"
    layout: str = "wide"
    initial_sidebar_state: str = "expanded"

@dataclass
class UIConfig:
    """Configuration for UI elements."""
    profile_photo_paths: Optional[List[str]] = None
    social_links: Optional[Dict[str, str]] = None
    
    def __post_init__(self):
        if self.profile_photo_paths is None:
            self.profile_photo_paths = ["phto.jpg", "assets/profile.jpg"]
        
        if self.social_links is None:
            self.social_links = {
                "LinkedIn": "https://www.linkedin.com/in/abdolamir-karbalaie-3bab9451/",
                "GitHub": "https://github.com/abdkar",
                "Google Scholar": "https://scholar.google.com/citations?user=Noi7TFUAAAA",
                "Web of Science": "https://www.webofscience.com/wos/author/record/B-6201-2016"
            }

@dataclass
class AppConfig:
    """Main application configuration."""
    knowledge_base_file: str = "knowledge_base.txt"
    uploaded_content_file: str = "uploaded_content.txt"
    env_file: str = ".env"
    log_directory: str = "logs"
    
    # Sub-configurations
    model: ModelConfig = ModelConfig()
    vector_store: VectorStoreConfig = VectorStoreConfig()
    server: ServerConfig = ServerConfig()
    ui: UIConfig = UIConfig()
    
    # Identity validation
    name_variations: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.name_variations is None:
            self.name_variations = [
                "Abdolamir Karbalaie",
                "abdolamir karbalaie", 
                "ABDOLAMIR KARBALAIE",
                "Abdolamir",
                "Amir",
                "amir",
                "Karbalaie"
            ]

# Global configuration instance
config = AppConfig()

# Environment variables
def get_google_api_key() -> str:
    """Get Google API key from environment variables."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    return api_key

# Prompt template
CHAT_PROMPT_TEMPLATE = """
You are the professional AI persona of Abdolamir ("Amir") Karbalaie. Use ONLY the Context. Do not invent or speculate.

Write naturally and concisely in third person ("he"). Do not say "according to the context." Quantify only when numbers appear in the Context.

If the question is identity/overview (e.g., "who is…", "tell me about…"), produce a polished 2–3 sentence paragraph. Otherwise, write one direct opening sentence followed by 3 compact bullets with **Bold labels** (≤2 words) and a colon.

If the needed facts are missing: "I do not have that information in the current context."
If the question is personal/out-of-scope (contact, family, salary, religion, politics):
"I do not have information on that topic. For details, it would be best to speak with Abdolamir directly."

Context
{context}

Question
{question}

Answer:
"""
