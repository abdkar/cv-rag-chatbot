"""
RAG Pipeline module for CV RAG Chatbot.
Handles the complete Retrieval Augmented Generation pipeline.
"""

import os
import sys
from datetime import datetime
from typing import Optional, Dict, Any

# Add the parent directory to sys.path to import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import streamlit as st

from configs.app_config import config, get_google_api_key, CHAT_PROMPT_TEMPLATE
from src.core.embeddings import get_embeddings
from src.utils.file_processing import load_knowledge_base, load_uploaded_content


class RAGPipeline:
    """
    Complete RAG pipeline for processing CV content and answering questions.
    """
    
    def __init__(self):
        """Initialize the RAG pipeline."""
        self.llm = None
        self.vectorstore = None
        self.qa_chain = None
        self.embeddings = None
        self.content_hash = None
        self.built_at = None
    
    def _initialize_llm(self) -> GoogleGenerativeAI:
        """
        Initialize the Google Gemini LLM.
        
        Returns:
            Configured GoogleGenerativeAI instance
        """
        # Configure Google AI
        api_key = get_google_api_key()
        genai.configure(api_key=api_key)
        
        # Initialize LLM
        return GoogleGenerativeAI(
            model=config.model.model_name,
            google_api_key=api_key,
            temperature=config.model.temperature,
            timeout=config.model.timeout
        )
    
    def _create_vector_store(self, content: str) -> FAISS:
        """
        Create FAISS vector store from content.
        
        Args:
            content: Text content to vectorize
            
        Returns:
            FAISS vector store
        """
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
    
    def _create_qa_chain(self) -> RetrievalQA:
        """
        Create the question-answering chain.
        
        Returns:
            Configured RetrievalQA chain
        """
        # Create custom prompt template
        custom_prompt = PromptTemplate(
            template=CHAT_PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )
        
        # Create QA chain
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": config.vector_store.search_k}
            ),
            return_source_documents=False,
            verbose=False,
            chain_type_kwargs={"prompt": custom_prompt}
        )
    
    def build_pipeline(self, use_uploaded: bool = False) -> Dict[str, Any]:
        """
        Build the complete RAG pipeline.
        
        Args:
            use_uploaded: Whether to use uploaded content or knowledge base
            
        Returns:
            Dictionary with pipeline components and metadata
        """
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
            self.llm = self._initialize_llm()
            self.vectorstore = self._create_vector_store(content_to_use)
            self.qa_chain = self._create_qa_chain()
            
            # Record build time
            self.built_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return {
                "chain": self.qa_chain,
                "content_hash": self.content_hash,
                "built_at": self.built_at,
                "content_length": len(content_to_use),
                "use_uploaded": use_uploaded
            }
            
        except Exception as e:
            st.error(f"❌ Error building RAG pipeline: {str(e)}")
            return None
    
    def query(self, question: str) -> str:
        """
        Query the RAG pipeline.
        
        Args:
            question: User question
            
        Returns:
            Generated response
        """
        if not self.qa_chain:
            return "❌ RAG pipeline not initialized. Please rebuild the pipeline."
        
        try:
            response = self.qa_chain.invoke({"query": question})
            
            # Handle different response formats from LangChain
            if isinstance(response, dict):
                response = response.get('result', str(response))
            
            if not response or (isinstance(response, str) and response.strip() == ""):
                return "I apologize, but I couldn't generate a response. This might be due to API limitations. Please try rephrasing your question or try again later."
            
            return response
            
        except Exception as e:
            if "quota" in str(e).lower() or "limit" in str(e).lower():
                return "⚠️ API quota exceeded. The free tier has daily limits. Please try again later or upgrade your API plan."
            else:
                return f"❌ Error: {str(e)}"


# Global pipeline instance for caching
_pipeline_cache = {}


@st.cache_resource
def get_rag_pipeline(content_hash: str, use_uploaded: bool = False) -> Optional[Dict[str, Any]]:
    """
    Get or create cached RAG pipeline.
    
    Args:
        content_hash: Hash of the content being used
        use_uploaded: Whether to use uploaded content
        
    Returns:
        RAG pipeline dictionary or None if failed
    """
    cache_key = f"{content_hash}_{use_uploaded}"
    
    if cache_key not in _pipeline_cache:
        pipeline = RAGPipeline()
        result = pipeline.build_pipeline(use_uploaded=use_uploaded)
        if result:
            result["pipeline"] = pipeline
            _pipeline_cache[cache_key] = result
        else:
            return None
    
    return _pipeline_cache[cache_key]


def clear_pipeline_cache():
    """Clear the pipeline cache."""
    global _pipeline_cache
    _pipeline_cache.clear()
    st.cache_resource.clear()
