"""
Simplified RAG Pipeline that works directly with Google Generative AI
without LangChain compatibility issues.
"""

import os
import sys
from datetime import datetime
from typing import Optional, Dict, Any

# Add the parent directory to sys.path to import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import streamlit as st

from configs.app_config import config, get_google_api_key, CHAT_PROMPT_TEMPLATE
from src.core.embeddings import get_embeddings
from src.utils.file_processing import load_knowledge_base, load_uploaded_content


class SimpleRAGPipeline:
    """
    Simplified RAG pipeline using direct Google AI integration.
    """
    
    def __init__(self):
        """Initialize the RAG pipeline."""
        self.model = None
        self.vectorstore = None
        self.embeddings = None
        self.content_hash = None
        self.built_at = None
    
    def _initialize_model(self):
        """Initialize the Google Gemini model directly."""
        api_key = get_google_api_key()
        genai.configure(api_key=api_key)
        
        # Try models in order of preference
        models_to_try = [config.model.model_name] + config.model.fallback_models
        
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                # Test with a minimal request
                response = model.generate_content(
                    "Hi", 
                    generation_config={'max_output_tokens': 5}
                )
                print(f"Successfully initialized model: {model_name}")
                return model
            except Exception as e:
                print(f"Failed to initialize {model_name}: {str(e)}")
                continue
        
        raise Exception("All models failed to initialize")
    
    def _create_vector_store(self, content: str) -> FAISS:
        """Create FAISS vector store from content."""
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.vector_store.chunk_size,
            chunk_overlap=config.vector_store.chunk_overlap,
            length_function=len
        )
        chunks = text_splitter.split_text(content)
        
        # Create embeddings if not already initialized
        if self.embeddings is None:
            self.embeddings = get_embeddings()
        
        # Create vector store
        return FAISS.from_texts(chunks, self.embeddings)
    
    def build_pipeline(self, use_uploaded: bool = False) -> Dict[str, Any]:
        """Build the complete RAG pipeline."""
        try:
            # Load content
            base_content = load_knowledge_base()
            content_to_use = base_content
            
            if use_uploaded:
                uploaded_content = load_uploaded_content()
                if uploaded_content:
                    content_to_use = uploaded_content
            
            # Generate content hash for caching
            from src.utils.file_processing import get_content_hash
            self.content_hash = get_content_hash(content_to_use)
            
            # Initialize components
            self.model = self._initialize_model()
            self.vectorstore = self._create_vector_store(content_to_use)
            
            # Record build time
            self.built_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return {
                "model": self.model,
                "vectorstore": self.vectorstore,
                "content_hash": self.content_hash,
                "built_at": self.built_at,
                "content_length": len(content_to_use),
                "use_uploaded": use_uploaded
            }
            
        except Exception as e:
            st.error(f"❌ Error building RAG pipeline: {str(e)}")
            return None
    
    def query(self, question: str) -> str:
        """Query the RAG pipeline."""
        if not self.model or not self.vectorstore:
            return "❌ RAG pipeline not initialized. Please rebuild the pipeline."
        
        try:
            # Retrieve relevant documents
            retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": config.vector_store.search_k}
            )
            docs = retriever.get_relevant_documents(question)
            
            # Prepare context
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Create prompt
            prompt = CHAT_PROMPT_TEMPLATE.format(context=context, question=question)
            
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': config.model.temperature,
                    'max_output_tokens': 1000
                }
            )
            
            return response.text
            
        except Exception as e:
            error_msg = str(e).lower()
            if "quota" in error_msg or "limit" in error_msg or "429" in error_msg:
                return "⚠️ API quota exceeded. The free tier has daily limits. Please try again later or upgrade your API plan."
            else:
                return f"❌ Error: {str(e)}"


# Global pipeline instance for caching
_simple_pipeline_cache = {}


@st.cache_resource
def get_simple_rag_pipeline(content_hash: str, use_uploaded: bool = False) -> Optional[Dict[str, Any]]:
    """Get or create cached simple RAG pipeline."""
    cache_key = f"{content_hash}_{use_uploaded}"
    
    if cache_key not in _simple_pipeline_cache:
        pipeline = SimpleRAGPipeline()
        result = pipeline.build_pipeline(use_uploaded=use_uploaded)
        if result:
            result["pipeline"] = pipeline
            _simple_pipeline_cache[cache_key] = result
        else:
            return None
    
    return _simple_pipeline_cache[cache_key]


def clear_simple_pipeline_cache():
    """Clear the simple pipeline cache."""
    global _simple_pipeline_cache
    _simple_pipeline_cache.clear()
    st.cache_resource.clear()
