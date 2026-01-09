"""
Similarity Calculator Module
Handles cosine similarity calculations between documents.
"""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple, Dict, Optional


class SimilarityCalculator:
    """Handles similarity calculations between document vectors."""
    
    def __init__(self):
        """Initialize the Similarity Calculator."""
        self.similarity_matrix = None
        self.document_vectors = None
    
    def calculate_similarity_matrix(self, vectors: np.ndarray) -> np.ndarray:
        """
        Calculate cosine similarity matrix for all documents.
        
        Args:
            vectors: Document vectors (TF-IDF matrix)
            
        Returns:
            Similarity matrix
        """
        self.document_vectors = vectors
        self.similarity_matrix = cosine_similarity(vectors)
        return self.similarity_matrix
    
    def calculate_pairwise_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Similarity score
        """
        # Reshape for sklearn
        vec1 = vec1.reshape(1, -1)
        vec2 = vec2.reshape(1, -1)
        
        return cosine_similarity(vec1, vec2)[0][0]
    
    def find_similar_documents(self, document_index: int, top_n: int = 3) -> List[Tuple[int, float]]:
        """
        Find most similar documents to a given document.
        
        Args:
            document_index: Index of the query document
            top_n: Number of similar documents to return
            
        Returns:
            List of (document_index, similarity_score) tuples
        """
        if self.similarity_matrix is None:
            raise ValueError("Similarity matrix not calculated. Call calculate_similarity_matrix first.")
        
        if document_index >= self.similarity_matrix.shape[0]:
            raise ValueError(f"Document index {document_index} out of range")
        
        # Get similarity scores for the document
        scores = self.similarity_matrix[document_index]
        
        # Get top similar documents (excluding the document itself)
        similar_indices = scores.argsort()[::-1][1:top_n+1]
        similar_docs = [(idx, scores[idx]) for idx in similar_indices]
        
        return similar_docs
    
    def find_most_similar_pairs(self, threshold: float = 0.5, top_n: int = 10) -> List[Tuple[int, int, float]]:
        """
        Find most similar document pairs above a threshold.
        
        Args:
            threshold: Minimum similarity score
            top_n: Maximum number of pairs to return
            
        Returns:
            List of (doc1_index, doc2_index, similarity_score) tuples
        """
        if self.similarity_matrix is None:
            raise ValueError("Similarity matrix not calculated. Call calculate_similarity_matrix first.")
        
        similar_pairs = []
        n_docs = self.similarity_matrix.shape[0]
        
        # Find pairs above threshold (avoid duplicates and self-comparisons)
        for i in range(n_docs):
            for j in range(i + 1, n_docs):
                similarity = self.similarity_matrix[i][j]
                if similarity >= threshold:
                    similar_pairs.append((i, j, similarity))
        
        # Sort by similarity score
        similar_pairs.sort(key=lambda x: x[2], reverse=True)
        
        return similar_pairs[:top_n]
    
    def calculate_cross_similarity(self, vectors1: np.ndarray, vectors2: np.ndarray) -> np.ndarray:
        """
        Calculate similarity between two sets of vectors.
        
        Args:
            vectors1: First set of vectors (e.g., cover letters)
            vectors2: Second set of vectors (e.g., job descriptions)
            
        Returns:
            Cross-similarity matrix
        """
        return cosine_similarity(vectors1, vectors2)
    
    def get_similarity_statistics(self) -> Dict:
        """
        Get statistics about the similarity matrix.
        
        Returns:
            Dictionary with similarity statistics
        """
        if self.similarity_matrix is None:
            return {}
        
        # Get upper triangle (excluding diagonal)
        upper_triangle = self.similarity_matrix[np.triu_indices(self.similarity_matrix.shape[0], k=1)]
        
        stats = {
            'matrix_shape': self.similarity_matrix.shape,
            'mean_similarity': np.mean(upper_triangle),
            'std_similarity': np.std(upper_triangle),
            'min_similarity': np.min(upper_triangle),
            'max_similarity': np.max(upper_triangle),
            'median_similarity': np.median(upper_triangle)
        }
        
        return stats
    
    def find_best_matches_for_query(self, query_vector: np.ndarray, document_vectors: np.ndarray, 
                                  top_n: int = 5) -> List[Tuple[int, float]]:
        """
        Find best matching documents for a query vector.
        
        Args:
            query_vector: Query document vector
            document_vectors: Document vectors to search
            top_n: Number of top matches to return
            
        Returns:
            List of (document_index, similarity_score) tuples
        """
        similarities = cosine_similarity(query_vector.reshape(1, -1), document_vectors)[0]
        
        # Get top matches
        top_indices = similarities.argsort()[::-1][:top_n]
        top_matches = [(idx, similarities[idx]) for idx in top_indices]
        
        return top_matches
    
    def cluster_documents_by_similarity(self, threshold: float = 0.7) -> List[List[int]]:
        """
        Simple clustering based on similarity threshold.
        
        Args:
            threshold: Similarity threshold for clustering
            
        Returns:
            List of clusters, each cluster is a list of document indices
        """
        if self.similarity_matrix is None:
            raise ValueError("Similarity matrix not calculated. Call calculate_similarity_matrix first.")
        
        n_docs = self.similarity_matrix.shape[0]
        visited = [False] * n_docs
        clusters = []
        
        for i in range(n_docs):
            if not visited[i]:
                # Start new cluster
                cluster = [i]
                visited[i] = True
                
                # Find similar documents
                for j in range(i + 1, n_docs):
                    if not visited[j] and self.similarity_matrix[i][j] >= threshold:
                        cluster.append(j)
                        visited[j] = True
                
                clusters.append(cluster)
        
        return clusters
    
    def export_similarity_matrix(self, filepath: str, document_labels: Optional[List[str]] = None) -> None:
        """
        Export similarity matrix to CSV file.
        
        Args:
            filepath: Path to save the CSV file
            document_labels: Optional labels for documents
        """
        if self.similarity_matrix is None:
            raise ValueError("Similarity matrix not calculated. Call calculate_similarity_matrix first.")
        
        df = pd.DataFrame(self.similarity_matrix)
        
        if document_labels:
            df.index = document_labels
            df.columns = document_labels
        
        df.to_csv(filepath)
        print(f"Similarity matrix exported to: {filepath}")


if __name__ == "__main__":
    # Example usage
    # Create sample vectors
    sample_vectors = np.array([
        [1.0, 0.5, 0.0, 0.0],
        [0.8, 0.6, 0.1, 0.0],
        [0.0, 0.0, 1.0, 0.8],
        [0.0, 0.0, 0.9, 0.7]
    ])
    
    # Initialize calculator
    calculator = SimilarityCalculator()
    
    # Calculate similarity matrix
    similarity_matrix = calculator.calculate_similarity_matrix(sample_vectors)
    print("Similarity Matrix:")
    print(similarity_matrix)
    print("\n" + "="*50 + "\n")
    
    # Find similar documents
    similar_docs = calculator.find_similar_documents(0, top_n=2)
    print("Documents similar to document 0:")
    for doc_idx, score in similar_docs:
        print(f"Document {doc_idx}: {score:.4f}")
    print("\n" + "="*50 + "\n")
    
    # Get statistics
    stats = calculator.get_similarity_statistics()
    print("Similarity Statistics:")
    for key, value in stats.items():
        print(f"{key}: {value:.4f}" if isinstance(value, float) else f"{key}: {value}")
    
    print("\n" + "="*50 + "\n")
    
    # Find similar pairs
    similar_pairs = calculator.find_most_similar_pairs(threshold=0.3)
    print("Most similar pairs:")
    for doc1, doc2, score in similar_pairs:
        print(f"Documents {doc1} and {doc2}: {score:.4f}")
