"""
Text Preprocessing Module
Handles text cleaning, tokenization, and preprocessing.
"""

import re
from typing import List, Set
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


class TextPreprocessor:
    """Handles text preprocessing for NLP analysis."""
    
    def __init__(self):
        """Initialize the Text Preprocessor."""
        try:
            import nltk
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('wordnet')
        except:
            print("Warning: NLTK data download failed. Some features may not work properly.")
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters
        text = re.sub(r'[^\w\s]', '', text)
        
        return text.strip()
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        return word_tokenize(text)
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Remove common stopwords from tokens."""
        stop_words = set(stopwords.words('english'))
        return [token for token in tokens if token.lower() not in stop_words]
    
    def stem_tokens(self, tokens: List[str]) -> List[str]:
        """Apply stemming to tokens."""
        stemmer = PorterStemmer()
        return [stemmer.stem(token) for token in tokens]
    
    def preprocess_text(self, text: str) -> List[str]:
        """Complete preprocessing pipeline."""
        # Clean text
        cleaned_text = self.clean_text(text)
        
        # Tokenize
        tokens = self.tokenize(cleaned_text)
        
        # Remove stopwords
        tokens = self.remove_stopwords(tokens)
        
        # Stem tokens
        tokens = self.stem_tokens(tokens)
        
        return tokens
    
    def get_text_statistics(self, text: str) -> dict:
        """Get basic statistics about the text."""
        tokens = self.preprocess_text(text)
        
        return {
            'word_count': len(tokens),
            'unique_words': len(set(tokens)),
            'avg_word_length': sum(len(word) for word in tokens) / len(tokens) if tokens else 0
        }
