"""
TF-IDF Vectorizer Module
Handles text vectorization using TF-IDF for similarity analysis.
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Tuple, Dict, Optional


class TFIDFVectorizer:
    """Handles TF-IDF vectorization and feature analysis."""
    
    def __init__(self, max_features: int = 5000, stop_words: str = 'english'):
        """
        Initialize the TF-IDF Vectorizer.
        
        Args:
            max_features: Maximum number of features to consider
            stop_words: Whether to use stop words ('english' or None)
        """
        self.max_features = max_features
        self.stop_words = stop_words
        self.vectorizer = None
        self.tfidf_matrix = None
        self.feature_names = None
    
    def fit_transform(self, documents: List[str]) -> np.ndarray:
        """
        Fit the vectorizer and transform documents to TF-IDF matrix.
        
        Args:
            documents: List of text documents
            
        Returns:
            TF-IDF matrix as numpy array
        """
        self.vectorizer = TfidfVectorizer(
            max_features=self.max_features,
            stop_words=self.stop_words
        )
        
        self.tfidf_matrix = self.vectorizer.fit_transform(documents)
        self.feature_names = self.vectorizer.get_feature_names_out()
        
        return self.tfidf_matrix.toarray()
    
    def transform(self, documents: List[str]) -> np.ndarray:
        """
        Transform new documents using the fitted vectorizer.
        
        Args:
            documents: List of text documents
            
        Returns:
            TF-IDF matrix as numpy array
        """
        if self.vectorizer is None:
            raise ValueError("Vectorizer not fitted. Call fit_transform first.")
        
        return self.vectorizer.transform(documents).toarray()
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance scores based on average TF-IDF scores.
        
        Returns:
            DataFrame with features and their importance scores
        """
        if self.tfidf_matrix is None:
            raise ValueError("TF-IDF matrix not available. Call fit_transform first.")
        
        # Calculate average TF-IDF score for each feature
        scores = np.asarray(self.tfidf_matrix.mean(axis=0)).ravel()
        
        importance_df = pd.DataFrame({
            "Keyword": self.feature_names,
            "Importance": scores
        }).sort_values(by="Importance", ascending=False)
        
        return importance_df
    
    def get_top_keywords(self, n: int = 20) -> pd.DataFrame:
        """
        Get top N keywords by importance.
        
        Args:
            n: Number of top keywords to return
            
        Returns:
            DataFrame with top keywords
        """
        importance_df = self.get_feature_importance()
        return importance_df.head(n)
    
    def get_document_keywords(self, document_index: int, top_n: int = 10) -> List[Tuple[str, float]]:
        """
        Get top keywords for a specific document.
        
        Args:
            document_index: Index of the document
            top_n: Number of top keywords to return
            
        Returns:
            List of (keyword, score) tuples
        """
        if self.tfidf_matrix is None:
            raise ValueError("TF-IDF matrix not available. Call fit_transform first.")
        
        if document_index >= self.tfidf_matrix.shape[0]:
            raise ValueError(f"Document index {document_index} out of range")
        
        # Get TF-IDF scores for the document
        doc_scores = self.tfidf_matrix[document_index].toarray().flatten()
        
        # Get top keywords
        top_indices = doc_scores.argsort()[::-1][:top_n]
        top_keywords = [
            (self.feature_names[i], doc_scores[i]) 
            for i in top_indices if doc_scores[i] > 0
        ]
        
        return top_keywords
    
    def get_vocabulary_size(self) -> int:
        """
        Get the size of the vocabulary.
        
        Returns:
            Number of unique features
        """
        if self.feature_names is None:
            return 0
        return len(self.feature_names)
    
    def get_matrix_shape(self) -> Tuple[int, int]:
        """
        Get the shape of the TF-IDF matrix.
        
        Returns:
            Tuple of (n_documents, n_features)
        """
        if self.tfidf_matrix is None:
            return (0, 0)
        return self.tfidf_matrix.shape
    
    def save_vectorizer(self, filepath: str) -> None:
        """
        Save the fitted vectorizer to a file.
        
        Args:
            filepath: Path to save the vectorizer
        """
        if self.vectorizer is None:
            raise ValueError("Vectorizer not fitted. Call fit_transform first.")
        
        import pickle
        with open(filepath, 'wb') as f:
            pickle.dump(self.vectorizer, f)
    
    def load_vectorizer(self, filepath: str) -> None:
        """
        Load a fitted vectorizer from a file.
        
        Args:
            filepath: Path to load the vectorizer from
        """
        import pickle
        with open(filepath, 'rb') as f:
            self.vectorizer = pickle.load(f)
        
        self.feature_names = self.vectorizer.get_feature_names_out()
    
    def get_vectorizer_info(self) -> Dict:
        """
        Get information about the vectorizer.
        
        Returns:
            Dictionary with vectorizer information
        """
        info = {
            'max_features': self.max_features,
            'stop_words': self.stop_words,
            'vocabulary_size': self.get_vocabulary_size(),
            'matrix_shape': self.get_matrix_shape()
        }
        
        if self.tfidf_matrix is not None:
            info['non_zero_elements'] = self.tfidf_matrix.nnz
            info['density'] = self.tfidf_matrix.nnz / (self.tfidf_matrix.shape[0] * self.tfidf_matrix.shape[1])
        
        return info


if __name__ == "__main__":
    # Example usage
    sample_docs = [
        "Software developer with Python experience",
        "Web developer skilled in JavaScript and React",
        "Data scientist using machine learning algorithms",
        "Full stack developer with database knowledge"
    ]
    
    # Initialize and fit vectorizer
    vectorizer = TFIDFVectorizer(max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(sample_docs)
    
    print("TF-IDF Matrix Shape:", tfidf_matrix.shape)
    print("\nTop Keywords:")
    print(vectorizer.get_top_keywords(10))
    
    print("\nVectorizer Info:")
    for key, value in vectorizer.get_vectorizer_info().items():
        print(f"{key}: {value}")
    
    print("\nKeywords for first document:")
    keywords = vectorizer.get_document_keywords(0, top_n=5)
    for keyword, score in keywords:
        print(f"{keyword}: {score:.4f}")
