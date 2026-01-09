"""
Cover Letter Matcher Module
Handles matching cover letters to job descriptions based on similarity.
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional
from data_loader import DataLoader
from preprocessing import TextPreprocessor
from vectorizer import TFIDFVectorizer
from similarity import SimilarityCalculator


class CoverLetterMatcher:
    """Main class for matching cover letters to job descriptions."""
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the Cover Letter Matcher.
        
        Args:
            data_dir: Base directory for data files
        """
        self.data_loader = DataLoader()
        self.preprocessor = TextPreprocessor()
        self.vectorizer = TFIDFVectorizer()
        self.similarity_calculator = SimilarityCalculator()
        
        # Data storage
        self.cover_letters = []
        self.job_descriptions = []
        self.processed_cover_letters = []
        self.processed_job_descriptions = []
        self.cover_letter_vectors = None
        self.job_description_vectors = None
        self.similarity_matrix = None
    
    def load_data(self, cover_letter_file: str = None, job_description_file: str = None) -> None:
        """
        Load cover letters and job descriptions.
        
        Args:
            cover_letter_file: Specific cover letter file (optional)
            job_description_file: Specific job description file (optional)
        """
        try:
            self.cover_letters = self.data_loader.load_cover_letters(cover_letter_file)
            self.job_descriptions = self.data_loader.load_job_descriptions(job_description_file)
            
            print(f"Loaded {len(self.cover_letters)} cover letters")
            print(f"Loaded {len(self.job_descriptions)} job descriptions")
            
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def preprocess_data(self, method: str = 'advanced') -> None:
        """
        Preprocess the loaded data.
        
        Args:
            method: Preprocessing method ('basic' or 'advanced')
        """
        if not self.cover_letters or not self.job_descriptions:
            raise ValueError("No data loaded. Call load_data first.")
        
        try:
            self.processed_cover_letters = self.preprocessor.preprocess_documents(
                self.cover_letters, method=method
            )
            self.processed_job_descriptions = self.preprocessor.preprocess_documents(
                self.job_descriptions, method=method
            )
            
            print(f"Preprocessed {len(self.processed_cover_letters)} cover letters")
            print(f"Preprocessed {len(self.processed_job_descriptions)} job descriptions")
            
            # Print statistics
            cl_stats = self.preprocessor.get_text_statistics(self.processed_cover_letters)
            jd_stats = self.preprocessor.get_text_statistics(self.processed_job_descriptions)
            
            print(f"Cover Letters - Avg words: {cl_stats.get('average_words_per_document', 0):.1f}")
            print(f"Job Descriptions - Avg words: {jd_stats.get('average_words_per_document', 0):.1f}")
            
        except Exception as e:
            raise Exception(f"Error preprocessing data: {str(e)}")
    
    def vectorize_data(self) -> None:
        """
        Vectorize the preprocessed data using TF-IDF.
        """
        if not self.processed_cover_letters or not self.processed_job_descriptions:
            raise ValueError("No preprocessed data available. Call preprocess_data first.")
        
        try:
            # Combine all documents for consistent vectorization
            all_docs = self.processed_cover_letters + self.processed_job_descriptions
            
            # Fit vectorizer on all documents
            tfidf_matrix = self.vectorizer.fit_transform(all_docs)
            
            # Split vectors back
            n_cover_letters = len(self.processed_cover_letters)
            self.cover_letter_vectors = tfidf_matrix[:n_cover_letters]
            self.job_description_vectors = tfidf_matrix[n_cover_letters:]
            
            print(f"Vectorized {len(self.cover_letter_vectors)} cover letters")
            print(f"Vectorized {len(self.job_description_vectors)} job descriptions")
            print(f"Feature vocabulary size: {self.vectorizer.get_vocabulary_size()}")
            
        except Exception as e:
            raise Exception(f"Error vectorizing data: {str(e)}")
    
    def calculate_similarity_matrix(self) -> None:
        """
        Calculate similarity matrix between cover letters and job descriptions.
        """
        if self.cover_letter_vectors is None or self.job_description_vectors is None:
            raise ValueError("No vectorized data available. Call vectorize_data first.")
        
        try:
            self.similarity_matrix = self.similarity_calculator.calculate_cross_similarity(
                self.cover_letter_vectors, self.job_description_vectors
            )
            
            print(f"Calculated similarity matrix: {self.similarity_matrix.shape}")
            
        except Exception as e:
            raise Exception(f"Error calculating similarity matrix: {str(e)}")
    
    def find_best_matches(self, job_description_index: int, top_n: int = 3) -> List[Tuple[int, float]]:
        """
        Find best matching cover letters for a job description.
        
        Args:
            job_description_index: Index of the job description
            top_n: Number of top matches to return
            
        Returns:
            List of (cover_letter_index, similarity_score) tuples
        """
        if self.similarity_matrix is None:
            raise ValueError("Similarity matrix not calculated. Call calculate_similarity_matrix first.")
        
        if job_description_index >= self.similarity_matrix.shape[1]:
            raise ValueError(f"Job description index {job_description_index} out of range")
        
        # Get similarity scores for the job description
        similarities = self.similarity_matrix[:, job_description_index]
        
        # Get top matches
        top_indices = similarities.argsort()[::-1][:top_n]
        top_matches = [(idx, similarities[idx]) for idx in top_indices]
        
        return top_matches
    
    def find_best_job_descriptions(self, cover_letter_index: int, top_n: int = 3) -> List[Tuple[int, float]]:
        """
        Find best matching job descriptions for a cover letter.
        
        Args:
            cover_letter_index: Index of the cover letter
            top_n: Number of top matches to return
            
        Returns:
            List of (job_description_index, similarity_score) tuples
        """
        if self.similarity_matrix is None:
            raise ValueError("Similarity matrix not calculated. Call calculate_similarity_matrix first.")
        
        if cover_letter_index >= self.similarity_matrix.shape[0]:
            raise ValueError(f"Cover letter index {cover_letter_index} out of range")
        
        # Get similarity scores for the cover letter
        similarities = self.similarity_matrix[cover_letter_index, :]
        
        # Get top matches
        top_indices = similarities.argsort()[::-1][:top_n]
        top_matches = [(idx, similarities[idx]) for idx in top_indices]
        
        return top_matches
    
    def get_match_report(self, cover_letter_index: int, job_description_index: int) -> Dict:
        """
        Get detailed match report between a cover letter and job description.
        
        Args:
            cover_letter_index: Index of the cover letter
            job_description_index: Index of the job description
            
        Returns:
            Dictionary with match details
        """
        if self.similarity_matrix is None:
            raise ValueError("Similarity matrix not calculated. Call calculate_similarity_matrix first.")
        
        similarity_score = self.similarity_matrix[cover_letter_index, job_description_index]
        
        # Get keywords for both documents
        cl_keywords = self.vectorizer.get_document_keywords(cover_letter_index, top_n=10)
        jd_keywords = self.vectorizer.get_document_keywords(
            len(self.processed_cover_letters) + job_description_index, top_n=10
        )
        
        return {
            'similarity_score': similarity_score,
            'cover_letter_index': cover_letter_index,
            'job_description_index': job_description_index,
            'cover_letter_keywords': cl_keywords,
            'job_description_keywords': jd_keywords,
            'cover_letter_preview': self.cover_letters[cover_letter_index][:200] + "...",
            'job_description_preview': self.job_descriptions[job_description_index][:200] + "..."
        }
    
    def get_top_matches_overall(self, top_n: int = 10) -> List[Tuple[int, int, float]]:
        """
        Get top matches across all cover letters and job descriptions.
        
        Args:
            top_n: Number of top matches to return
            
        Returns:
            List of (cover_letter_index, job_description_index, similarity_score) tuples
        """
        if self.similarity_matrix is None:
            raise ValueError("Similarity matrix not calculated. Call calculate_similarity_matrix first.")
        
        # Flatten the similarity matrix and get top matches
        matches = []
        for i in range(self.similarity_matrix.shape[0]):
            for j in range(self.similarity_matrix.shape[1]):
                matches.append((i, j, self.similarity_matrix[i, j]))
        
        # Sort by similarity score
        matches.sort(key=lambda x: x[2], reverse=True)
        
        return matches[:top_n]
    
    def export_matches_to_csv(self, output_path: str, top_n: int = 50) -> None:
        """
        Export top matches to CSV file.
        
        Args:
            output_path: Path to save the CSV file
            top_n: Number of top matches to export
        """
        if self.similarity_matrix is None:
            raise ValueError("Similarity matrix not calculated. Call calculate_similarity_matrix first.")
        
        top_matches = self.get_top_matches_overall(top_n)
        
        # Create DataFrame
        match_data = []
        for cl_idx, jd_idx, score in top_matches:
            match_data.append({
                'cover_letter_index': cl_idx,
                'job_description_index': jd_idx,
                'similarity_score': score,
                'cover_letter_preview': self.cover_letters[cl_idx][:100] + "...",
                'job_description_preview': self.job_descriptions[jd_idx][:100] + "..."
            })
        
        df = pd.DataFrame(match_data)
        df.to_csv(output_path, index=False)
        print(f"Matches exported to: {output_path}")
    
    def run_full_pipeline(self, cover_letter_file: str = None, 
                         job_description_file: str = None,
                         preprocessing_method: str = 'advanced') -> None:
        """
        Run the complete matching pipeline.
        
        Args:
            cover_letter_file: Specific cover letter file (optional)
            job_description_file: Specific job description file (optional)
            preprocessing_method: Preprocessing method to use
        """
        print("Starting cover letter matching pipeline...")
        
        # Load data
        print("\n1. Loading data...")
        self.load_data(cover_letter_file, job_description_file)
        
        # Preprocess data
        print("\n2. Preprocessing data...")
        self.preprocess_data(method=preprocessing_method)
        
        # Vectorize data
        print("\n3. Vectorizing data...")
        self.vectorize_data()
        
        # Calculate similarity
        print("\n4. Calculating similarities...")
        self.calculate_similarity_matrix()
        
        print("\nPipeline completed successfully!")
        
        # Show top matches
        top_matches = self.get_top_matches_overall(5)
        print("\nTop 5 matches:")
        for cl_idx, jd_idx, score in top_matches:
            print(f"Cover Letter {cl_idx} - Job Description {jd_idx}: {score:.4f}")


if __name__ == "__main__":
    # Example usage
    matcher = CoverLetterMatcher()
    
    try:
        # Run full pipeline
        matcher.run_full_pipeline()
        
        # Find best matches for first job description
        print("\nBest matches for Job Description 0:")
        matches = matcher.find_best_matches(0, top_n=3)
        for cl_idx, score in matches:
            print(f"Cover Letter {cl_idx}: {score:.4f}")
        
        # Get detailed match report
        print("\nDetailed match report:")
        report = matcher.get_match_report(0, 0)
        print(f"Similarity Score: {report['similarity_score']:.4f}")
        print(f"Cover Letter Keywords: {[kw for kw, _ in report['cover_letter_keywords'][:5]]}")
        print(f"Job Description Keywords: {[kw for kw, _ in report['job_description_keywords'][:5]]}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
