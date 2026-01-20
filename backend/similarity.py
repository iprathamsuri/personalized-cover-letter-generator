"""
Similarity Calculator Module
Handles cosine similarity calculations between documents.
"""

import numpy as np
from typing import List, Tuple
from sklearn.metrics.pairwise import cosine_similarity


class SimilarityCalculator:
    """Calculates similarity between documents using cosine similarity."""
    
    def __init__(self):
        """Initialize the Similarity Calculator."""
        pass
    
    def calculate_similarity_matrix(self, tfidf_matrix: np.ndarray) -> np.ndarray:
        """Calculate cosine similarity matrix."""
        return cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    def get_most_similar_documents(self, similarity_matrix: np.ndarray, 
                                  document_index: int, top_n: int = 5) -> List[Tuple[int, float]]:
        """Get most similar documents to a given document."""
        similarity_scores = similarity_matrix[document_index]
        similar_indices = np.argsort(similarity_scores)[::-1][:top_n]
        
        return [(i, float(similarity_scores[i])) for i in similar_indices]
    
    def get_similarity_statistics(self, similarity_matrix: np.ndarray) -> dict:
        """Get statistics about similarity matrix."""
        return {
            'mean_similarity': np.mean(similarity_matrix),
            'max_similarity': np.max(similarity_matrix),
            'min_similarity': np.min(similarity_matrix),
            'std_similarity': np.std(similarity_matrix)
        }
