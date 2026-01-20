"""
Cover Letter Matcher Module
Orchestrates the entire NLP pipeline for matching cover letters to job descriptions.
"""

from typing import List, Tuple, Dict
from .data_loader import DataLoader
from .preprocessing import TextPreprocessor
from .vectorizer import TFIDFVectorizer
from .similarity import SimilarityCalculator


class CoverLetterMatcher:
    """Matches cover letters to job descriptions using NLP techniques."""
    
    def __init__(self, cover_letter_dir: str = None, job_description_dir: str = None):
        """Initialize the Cover Letter Matcher."""
        self.data_loader = DataLoader(cover_letter_dir, job_description_dir)
        self.preprocessor = TextPreprocessor()
        self.vectorizer = TFIDFVectorizer()
        self.similarity_calculator = SimilarityCalculator()
        
        # Load data
        self.cover_letters = self.data_loader.load_cover_letters()
        self.job_descriptions = self.data_loader.load_job_descriptions()
        
        # Process documents
        self.processed_cover_letters = []
        self.processed_job_descriptions = []
        
        if self.cover_letters:
            self.processed_cover_letters = self.preprocessor.preprocess_text(' '.join(self.cover_letters))
        
        if self.job_descriptions:
            self.processed_job_descriptions = self.preprocessor.preprocess_text(' '.join(self.job_descriptions))
        
        # Create TF-IDF vectors
        if self.processed_job_descriptions:
            self.tfidf_matrix, self.feature_names = self.vectorizer.fit_transform(self.processed_job_descriptions)
        
        # Calculate similarity matrix
        self.similarity_matrix = None
    
    def match_cover_letter_to_job_description(self, job_description: str, top_n: int = 5) -> List[Tuple[int, float]]:
        """Match cover letters to a job description."""
        if not self.processed_job_descriptions:
            return []
        
        # Vectorize job description
        processed_jd = self.preprocessor.preprocess_text(job_description)
        jd_vector = self.vectorizer.vectorizer.transform([processed_jd])
        
        # Calculate similarities
        similarities = self.similarity_calculator.calculate_similarity_matrix(
            self.tfidf_matrix, jd_vector
        ).flatten()
        
        # Get top matches
        top_matches = []
        for i, similarity in enumerate(similarities):
            if i < len(self.cover_letters):
                top_matches.append((i, float(similarity)))
        
        # Sort by similarity and return top N
        top_matches.sort(key=lambda x: x[1], reverse=True)
        
        return top_matches[:top_n]
    
    def get_matching_info(self, job_description: str, top_n: int = 5) -> Dict[str, any]:
        """Get detailed matching information."""
        matches = self.match_cover_letter_to_job_description(job_description, top_n)
        
        return {
            'matches': matches,
            'total_cover_letters': len(self.cover_letters),
            'total_job_descriptions': len(self.job_descriptions),
            'top_n': top_n
        }
    
    def get_best_match_content(self, job_description: str, top_n: int = 3) -> str:
        """Get best matching content for cover letter generation."""
        matches = self.match_cover_letter_to_job_description(job_description, top_n)
        
        if not matches:
            return ""
        
        # Get content from top matches
        best_content = []
        for idx, similarity in matches[:top_n]:
            if idx < len(self.cover_letters):
                content = self.cover_letters[idx]
                # Extract key sentences (first few sentences)
                sentences = content.split('. ')[:3]
                best_content.extend(sentences)
        
        return '. '.join(best_content)
