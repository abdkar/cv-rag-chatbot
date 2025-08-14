"""
Embeddings module for CV RAG Chatbot.
Provides simple hash-based embeddings for maximum compatibility.
"""

import re
from typing import List, Union, Optional
import sys
import os

# Add the parent directory to sys.path to import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from configs.app_config import config


class SimpleHashEmbeddings:
    """
    Simple hash-based embeddings using only built-in Python libraries.
    Provides deterministic embeddings without external dependencies.
    """
    
    def __init__(self, dimension: Optional[int] = None):
        """Initialize embeddings with specified dimension."""
        self.dimension = dimension or config.model.embedding_dimension
    
    def _text_to_vector(self, text: str) -> List[float]:
        """
        Convert text to vector using hash-based approach.
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the text embedding
        """
        if not text:
            return [0.0] * self.dimension
        
        # Clean and tokenize text
        words = re.findall(r'\w+', text.lower())
        
        # Create a simple hash-based vector
        vector = [0.0] * self.dimension
        for word in words[:self.dimension]:
            # Use hash to create pseudo-random but deterministic values
            hash_val = hash(word) % self.dimension
            vector[hash_val] += 1.0
        
        # Simple normalization
        total = sum(vector)
        if total > 0:
            vector = [x/total for x in vector]
        
        return vector
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents.
        
        Args:
            texts: List of text documents to embed
            
        Returns:
            List of embedding vectors
        """
        return [self._text_to_vector(text) for text in texts]
    
    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query text.
        
        Args:
            text: Query text to embed
            
        Returns:
            Embedding vector for the query
        """
        return self._text_to_vector(text)
    
    def __call__(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """
        Make the embeddings object callable for FAISS compatibility.
        
        Args:
            text: Single text string or list of texts
            
        Returns:
            Single embedding vector or list of embedding vectors
        """
        if isinstance(text, list):
            return self.embed_documents(text)
        else:
            return self.embed_query(text)


def get_embeddings() -> SimpleHashEmbeddings:
    """
    Factory function to get embeddings instance.
    
    Returns:
        Configured embeddings instance
    """
    return SimpleHashEmbeddings()
