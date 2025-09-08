"""
Hybrid Search Engine for Yeneta RAG Platform

This module implements a hybrid search engine that combines:
- Semantic search using vector embeddings
- Keyword search using BM25
- Cross-encoder reranking for improved accuracy
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from sentence_transformers import SentenceTransformer, CrossEncoder
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import chromadb
from chromadb.config import Settings
import logging

logger = logging.getLogger(__name__)

class HybridSearchEngine:
    """
    Advanced hybrid search engine that combines multiple retrieval methods
    for improved accuracy and relevance in educational content.
    """
    
    def __init__(self, 
                 embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
                 cross_encoder_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
                 persist_directory: str = "./chroma_store"):
        """
        Initialize the hybrid search engine.
        
        Args:
            embedding_model: HuggingFace model for embeddings
            cross_encoder_model: Cross-encoder model for reranking
            persist_directory: Directory to persist ChromaDB
        """
        self.embedding_model = embedding_model
        self.cross_encoder_model = cross_encoder_model
        self.persist_directory = persist_directory
        
        # Initialize components
        self._setup_embeddings()
        self._setup_cross_encoder()
        self._setup_vector_store()
        self._setup_text_splitter()
        
        logger.info("HybridSearchEngine initialized successfully")
    
    def _setup_embeddings(self):
        """Setup embedding model"""
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.embedding_model,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            logger.info(f"Embeddings model loaded: {self.embedding_model}")
        except Exception as e:
            logger.error(f"Failed to load embeddings model: {e}")
            raise
    
    def _setup_cross_encoder(self):
        """Setup cross-encoder for reranking"""
        try:
            self.cross_encoder = CrossEncoder(self.cross_encoder_model)
            logger.info(f"Cross-encoder model loaded: {self.cross_encoder_model}")
        except Exception as e:
            logger.error(f"Failed to load cross-encoder model: {e}")
            raise
    
    def _setup_vector_store(self):
        """Setup ChromaDB vector store"""
        try:
            # Initialize ChromaDB client
            self.chroma_client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            self.collection = self.chroma_client.get_or_create_collection(
                name="yeneta_educational_content",
                metadata={"description": "Educational content for Yeneta platform"}
            )
            
            logger.info("ChromaDB vector store initialized")
        except Exception as e:
            logger.error(f"Failed to setup vector store: {e}")
            raise
    
    def _setup_text_splitter(self):
        """Setup text splitter for document processing"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def add_documents(self, documents: List[Document]) -> bool:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of LangChain Document objects
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            # Prepare data for ChromaDB
            texts = [chunk.page_content for chunk in chunks]
            metadatas = [chunk.metadata for chunk in chunks]
            ids = [f"chunk_{i}" for i in range(len(chunks))]
            
            # Generate embeddings
            embeddings = self.embeddings.embed_documents(texts)
            
            # Add to ChromaDB
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(chunks)} document chunks to vector store")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            return False
    
    def semantic_search(self, query: str, k: int = 10) -> List[Dict[str, Any]]:
        """
        Perform semantic search using vector embeddings.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of search results with scores
        """
        try:
            # Generate query embedding
            query_embedding = self.embeddings.embed_query(query)
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k
            )
            
            # Format results
            search_results = []
            for i in range(len(results['documents'][0])):
                search_results.append({
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'score': results['distances'][0][i],
                    'id': results['ids'][0][i]
                })
            
            return search_results
            
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return []
    
    def keyword_search(self, query: str, k: int = 10) -> List[Dict[str, Any]]:
        """
        Perform keyword search using BM25-like approach.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of search results with scores
        """
        try:
            # Simple keyword matching (in a real implementation, you'd use BM25)
            query_terms = query.lower().split()
            
            # Get all documents
            all_docs = self.collection.get()
            
            # Score documents based on keyword matches
            scored_docs = []
            for i, doc in enumerate(all_docs['documents']):
                doc_terms = doc.lower().split()
                score = sum(1 for term in query_terms if term in doc_terms)
                
                if score > 0:
                    scored_docs.append({
                        'content': doc,
                        'metadata': all_docs['metadatas'][i],
                        'score': score,
                        'id': all_docs['ids'][i]
                    })
            
            # Sort by score and return top k
            scored_docs.sort(key=lambda x: x['score'], reverse=True)
            return scored_docs[:k]
            
        except Exception as e:
            logger.error(f"Keyword search failed: {e}")
            return []
    
    def rerank_results(self, query: str, results: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Rerank search results using cross-encoder.
        
        Args:
            query: Original search query
            results: List of search results to rerank
            top_k: Number of top results to return
            
        Returns:
            Reranked list of results
        """
        try:
            if not results:
                return []
            
            # Prepare query-document pairs for cross-encoder
            pairs = [(query, result['content']) for result in results]
            
            # Get relevance scores
            relevance_scores = self.cross_encoder.predict(pairs)
            
            # Add scores to results
            for i, result in enumerate(results):
                result['relevance_score'] = float(relevance_scores[i])
            
            # Sort by relevance score
            reranked_results = sorted(results, key=lambda x: x['relevance_score'], reverse=True)
            
            return reranked_results[:top_k]
            
        except Exception as e:
            logger.error(f"Reranking failed: {e}")
            return results[:top_k]  # Return original results if reranking fails
    
    def hybrid_search(self, query: str, k: int = 10, semantic_weight: float = 0.7) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining semantic and keyword search.
        
        Args:
            query: Search query
            k: Number of results to return
            semantic_weight: Weight for semantic search (0.0 to 1.0)
            
        Returns:
            List of hybrid search results
        """
        try:
            # Perform both searches
            semantic_results = self.semantic_search(query, k)
            keyword_results = self.keyword_search(query, k)
            
            # Combine results
            combined_results = {}
            
            # Add semantic results
            for result in semantic_results:
                doc_id = result['id']
                combined_results[doc_id] = {
                    'content': result['content'],
                    'metadata': result['metadata'],
                    'semantic_score': result['score'],
                    'keyword_score': 0.0,
                    'id': doc_id
                }
            
            # Add keyword results
            for result in keyword_results:
                doc_id = result['id']
                if doc_id in combined_results:
                    combined_results[doc_id]['keyword_score'] = result['score']
                else:
                    combined_results[doc_id] = {
                        'content': result['content'],
                        'metadata': result['metadata'],
                        'semantic_score': 0.0,
                        'keyword_score': result['score'],
                        'id': doc_id
                    }
            
            # Calculate hybrid scores
            for doc_id, result in combined_results.items():
                hybrid_score = (
                    semantic_weight * result['semantic_score'] +
                    (1 - semantic_weight) * result['keyword_score']
                )
                result['hybrid_score'] = hybrid_score
            
            # Sort by hybrid score
            final_results = list(combined_results.values())
            final_results.sort(key=lambda x: x['hybrid_score'], reverse=True)
            
            # Rerank top results
            top_results = final_results[:k*2]  # Get more for reranking
            reranked_results = self.rerank_results(query, top_results, k)
            
            return reranked_results
            
        except Exception as e:
            logger.error(f"Hybrid search failed: {e}")
            return []
    
    def search(self, query: str, search_type: str = "hybrid", k: int = 10) -> List[Dict[str, Any]]:
        """
        Main search method that delegates to appropriate search type.
        
        Args:
            query: Search query
            search_type: Type of search ("semantic", "keyword", "hybrid")
            k: Number of results to return
            
        Returns:
            List of search results
        """
        if search_type == "semantic":
            return self.semantic_search(query, k)
        elif search_type == "keyword":
            return self.keyword_search(query, k)
        elif search_type == "hybrid":
            return self.hybrid_search(query, k)
        else:
            logger.warning(f"Unknown search type: {search_type}, using hybrid")
            return self.hybrid_search(query, k)
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the document collection.
        
        Returns:
            Dictionary with collection statistics
        """
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "embedding_model": self.embedding_model,
                "cross_encoder_model": self.cross_encoder_model,
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {}
    
    def reset_collection(self) -> bool:
        """
        Reset the document collection (delete all documents).
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.chroma_client.delete_collection("yeneta_educational_content")
            self.collection = self.chroma_client.create_collection(
                name="yeneta_educational_content",
                metadata={"description": "Educational content for Yeneta platform"}
            )
            logger.info("Collection reset successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to reset collection: {e}")
            return False
