"""
TF-IDF Vectorizer Module
Handles TF-IDF vectorization of documents.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Tuple


class TFIDFVectorizer:
    """Handles TF-IDF vectorization of documents."""
    
    def __init__(self, max_features: int = 5000, max_df: float = 0.7):
        """Initialize the TF-IDF Vectorizer."""
        self.max_features = max_features
        self.max_df = max_df
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            max_df=max_df,
            stop_words='english',
            lowercase=True,
            ngram_range=(1, 2)
        )
    
    def fit_transform(self, documents: List[str]) -> Tuple[np.ndarray, List[str]]:
        """Fit TF-IDF vectorizer on documents and transform them."""
        tfidf_matrix = self.vectorizer.fit_transform(documents)
        feature_names = self.vectorizer.get_feature_names_out()
        
        return tfidf_matrix, feature_names
    
    def get_vocabulary_size(self) -> int:
        """Get the size of the vocabulary."""
        return len(self.vectorizer.vocabulary_)
    
    def get_top_keywords(self, tfidf_matrix: np.ndarray, feature_names: List[str], 
                      top_n: int = 10) -> List[Tuple[str, float]]:
        """Get top keywords from TF-IDF matrix."""
        # Get mean TF-IDF scores across all documents
        mean_scores = np.mean(tfidf_matrix, axis=0)
        
        # Get top keywords
        top_keywords = []
        for i, feature_name in enumerate(feature_names):
            score = mean_scores[i]
            top_keywords.append((feature_name, score))
        
        # Sort by score and return top N
        top_keywords.sort(key=lambda x: x[1], reverse=True)
        
        return top_keywords[:top_n]
