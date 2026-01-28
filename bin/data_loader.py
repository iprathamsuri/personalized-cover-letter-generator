"""
Data Loader Module
Handles loading of cover letters and job descriptions from files.
"""

import os
from typing import List, Optional
from pathlib import Path


class DataLoader:
    """Handles loading of cover letters and job descriptions from files."""
    
    def __init__(self, cover_letter_dir: str = None, job_description_dir: str = None):
        """Initialize the Data Loader."""
        self.cover_letter_dir = cover_letter_dir or self._get_default_cover_letter_dir()
        self.job_description_dir = job_description_dir or self._get_default_job_description_dir()
    
    def _get_default_cover_letter_dir(self) -> str:
        """Get default cover letter directory."""
        return os.path.join(os.path.dirname(__file__), 'sample_data', 'cover_letter_data')
    
    def _get_default_job_description_dir(self) -> str:
        """Get default job description directory."""
        return os.path.join(os.path.dirname(__file__), 'sample_data', 'job_description_data')
    
    def load_cover_letters(self) -> List[str]:
        """Load all cover letters from the directory."""
        cover_letters = []
        cover_letter_dir = Path(self.cover_letter_dir)
        
        if cover_letter_dir.exists():
            for file_path in cover_letter_dir.glob("*.txt"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    cover_letters.append(content)
        
        return cover_letters
    
    def load_job_descriptions(self) -> List[str]:
        """Load all job descriptions from the directory."""
        job_descriptions = []
        job_description_dir = Path(self.job_description_dir)
        
        if job_description_dir.exists():
            for file_path in job_description_dir.glob("*.txt"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    job_descriptions.append(content)
        
        return job_descriptions
    
    def split_documents(self, documents: List[str]) -> List[List[str]]:
        """Split documents into sentences and words."""
        split_docs = []
        for doc in documents:
            # Simple sentence splitting
            sentences = doc.split('. ')
            words = doc.split()
            split_docs.append([sentences, words])
        
        return split_docs
    
    def get_default_file_paths(self) -> dict:
        """Get default file paths for cover letters and job descriptions."""
        return {
            'cover_letters': self._get_default_cover_letter_dir(),
            'job_descriptions': self._get_default_job_description_dir()
        }
