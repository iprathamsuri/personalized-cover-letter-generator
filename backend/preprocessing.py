"""
Text Preprocessing Module
Handles text cleaning, normalization, and preprocessing for cover letters and job descriptions.
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from typing import List


class TextPreprocessor:
    """Handles text preprocessing and cleaning operations."""
    
    def __init__(self, download_nltk_data: bool = True):
        """
        Initialize the TextPreprocessor.
        
        Args:
            download_nltk_data: Whether to download required NLTK data
        """
        if download_nltk_data:
            self._download_nltk_data()
        
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
    
    def _download_nltk_data(self) -> None:
        """Download required NLTK data packages."""
        try:
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('punkt', quiet=True)
        except Exception as e:
            print(f"Warning: Could not download NLTK data: {str(e)}")
    
    def clean_text_basic(self, text: str) -> str:
        """
        Basic text cleaning - removes emails, phone numbers, punctuation, and digits.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove emails
        text = re.sub(r"\S+@\S+", " ", text)
        
        # Remove phone numbers
        text = re.sub(r"\+?\d[\d\s\-()]{7,}", " ", text)
        
        # Remove punctuation and digits, keep only letters and spaces
        text = re.sub(r"[^a-z\s]", " ", text)
        
        # Remove extra spaces and normalize
        text = re.sub(r"\s+", " ", text).strip()
        
        return text
    
    def clean_text_advanced(self, text: str) -> str:
        """
        Advanced text cleaning with stopword removal and lemmatization.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned and processed text
        """
        # First apply basic cleaning
        text = self.clean_text_basic(text)
        
        # Tokenize
        tokens = text.split()
        
        # Remove stopwords and short words
        tokens = [w for w in tokens if w not in self.stop_words and len(w) > 2]
        
        # Lemmatize
        tokens = [self.lemmatizer.lemmatize(w) for w in tokens]
        
        # Join back to text
        return " ".join(tokens)
    
    def analyze_text_keywords(self, text: str) -> str:
        """
        Analyze text and return processed keywords (alias for advanced cleaning).
        
        Args:
            text: Text to analyze
            
        Returns:
            Processed keyword string
        """
        return self.clean_text_advanced(text)
    
    def preprocess_documents(self, documents: List[str], method: str = 'advanced') -> List[str]:
        """
        Preprocess a list of documents.
        
        Args:
            documents: List of text documents to preprocess
            method: Preprocessing method ('basic' or 'advanced')
            
        Returns:
            List of preprocessed documents
        """
        if method == 'basic':
            return [self.clean_text_basic(doc) for doc in documents]
        elif method == 'advanced':
            return [self.clean_text_advanced(doc) for doc in documents]
        else:
            raise ValueError("Method must be 'basic' or 'advanced'")
    
    def get_text_statistics(self, documents: List[str]) -> dict:
        """
        Get basic statistics about the processed documents.
        
        Args:
            documents: List of processed documents
            
        Returns:
            Dictionary with text statistics
        """
        if not documents:
            return {}
        
        total_docs = len(documents)
        total_words = sum(len(doc.split()) for doc in documents)
        avg_words_per_doc = total_words / total_docs if total_docs > 0 else 0
        
        # Get all unique words
        all_words = set()
        for doc in documents:
            all_words.update(doc.split())
        
        return {
            'total_documents': total_docs,
            'total_words': total_words,
            'average_words_per_document': avg_words_per_doc,
            'unique_vocabulary_size': len(all_words)
        }
    
    def filter_documents_by_length(self, documents: List[str], min_length: int = 50, max_length: int = 5000) -> List[str]:
        """
        Filter documents by word count length.
        
        Args:
            documents: List of documents to filter
            min_length: Minimum word count
            max_length: Maximum word count
            
        Returns:
            Filtered list of documents
        """
        filtered_docs = []
        for doc in documents:
            word_count = len(doc.split())
            if min_length <= word_count <= max_length:
                filtered_docs.append(doc)
        
        return filtered_docs


if __name__ == "__main__":
    # Example usage
    preprocessor = TextPreprocessor()
    
    # Sample text
    sample_text = """
    Hello, I would like to apply to your Software Developer position. 
    Contact me at john.doe@email.com or call +1-555-123-4567. 
    I have 5 years of experience in Python development and web technologies.
    """
    
    print("Original text:")
    print(sample_text)
    print("\n" + "="*50 + "\n")
    
    # Basic cleaning
    basic_clean = preprocessor.clean_text_basic(sample_text)
    print("Basic cleaning:")
    print(basic_clean)
    print("\n" + "="*50 + "\n")
    
    # Advanced cleaning
    advanced_clean = preprocessor.clean_text_advanced(sample_text)
    print("Advanced cleaning:")
    print(advanced_clean)
    print("\n" + "="*50 + "\n")
    
    # Statistics
    sample_docs = [basic_clean, advanced_clean]
    stats = preprocessor.get_text_statistics(sample_docs)
    print("Document Statistics:")
    for key, value in stats.items():
        print(f"{key}: {value}")
