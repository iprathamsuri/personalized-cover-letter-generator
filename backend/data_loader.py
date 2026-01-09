"""
Data Loader Module
Handles loading and parsing of cover letters and job descriptions from text files.
"""

import os
import re
from typing import List, Tuple


class DataLoader:
    """Handles loading and parsing of cover letters and job descriptions."""
    
    def __init__(self, cover_letter_dir: str = None, job_description_dir: str = None):
        """
        Initialize the DataLoader.
        
        Args:
            cover_letter_dir: Path to directory containing cover letter files
            job_description_dir: Path to directory containing job description files
        """
        self.cover_letter_dir = cover_letter_dir or "sample_data/cover_letter_data"
        self.job_description_dir = job_description_dir or "sample_data/job_description_data"
    
    def load_text_file(self, file_path: str) -> str:
        """
        Load text content from a file.
        
        Args:
            file_path: Path to the text file
            
        Returns:
            Raw text content from the file
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error loading file {file_path}: {str(e)}")
    
    def split_documents(self, raw_text: str, min_length: int = 150) -> List[str]:
        """
        Split raw text into individual documents using underscore separators.
        
        Args:
            raw_text: Raw text containing multiple documents
            min_length: Minimum document length to be considered valid
            
        Returns:
            List of document strings
        """
        documents = re.split(r'_{10,}', raw_text)
        documents = [doc.strip() for doc in documents if len(doc.strip()) > min_length]
        return documents
    
    def load_cover_letters(self, file_name: str = None) -> List[str]:
        """
        Load and parse cover letters from text files.
        
        Args:
            file_name: Specific file name to load (optional)
            
        Returns:
            List of cover letter strings
        """
        if file_name:
            file_path = os.path.join(self.cover_letter_dir, file_name)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Cover letter file not found: {file_path}")
            raw_text = self.load_text_file(file_path)
            return self.split_documents(raw_text)
        
        # Load all files in directory
        cover_letters = []
        if os.path.exists(self.cover_letter_dir):
            for filename in os.listdir(self.cover_letter_dir):
                if filename.endswith('.txt'):
                    file_path = os.path.join(self.cover_letter_dir, filename)
                    try:
                        raw_text = self.load_text_file(file_path)
                        documents = self.split_documents(raw_text)
                        cover_letters.extend(documents)
                    except Exception as e:
                        print(f"Warning: Could not process {filename}: {str(e)}")
        
        return cover_letters
    
    def load_job_descriptions(self, file_name: str = None) -> List[str]:
        """
        Load and parse job descriptions from text files.
        
        Args:
            file_name: Specific file name to load (optional)
            
        Returns:
            List of job description strings
        """
        if file_name:
            file_path = os.path.join(self.job_description_dir, file_name)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Job description file not found: {file_path}")
            raw_text = self.load_text_file(file_path)
            return self.split_documents(raw_text)
        
        # Load all files in directory
        job_descriptions = []
        if os.path.exists(self.job_description_dir):
            for filename in os.listdir(self.job_description_dir):
                if filename.endswith('.txt'):
                    file_path = os.path.join(self.job_description_dir, filename)
                    try:
                        raw_text = self.load_text_file(file_path)
                        documents = self.split_documents(raw_text)
                        job_descriptions.extend(documents)
                    except Exception as e:
                        print(f"Warning: Could not process {filename}: {str(e)}")
        
        return job_descriptions
    
    def load_all_data(self) -> Tuple[List[str], List[str]]:
        """
        Load both cover letters and job descriptions.
        
        Returns:
            Tuple of (cover_letters, job_descriptions)
        """
        cover_letters = self.load_cover_letters()
        job_descriptions = self.load_job_descriptions()
        
        return cover_letters, job_descriptions
    
    def save_processed_data(self, data: List[str], output_path: str) -> None:
        """
        Save processed data to a text file.
        
        Args:
            data: List of text strings to save
            output_path: Path to save the processed data
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                for item in data:
                    f.write(item + "\n\n")
            print(f"Data saved successfully to: {output_path}")
        except Exception as e:
            raise Exception(f"Error saving data to {output_path}: {str(e)}")


if __name__ == "__main__":
    # Example usage
    loader = DataLoader()
    
    try:
        cover_letters, job_descriptions = loader.load_all_data()
        print(f"Loaded {len(cover_letters)} cover letters")
        print(f"Loaded {len(job_descriptions)} job descriptions")
        
        # Save processed data
        loader.save_processed_data(cover_letters, "processed_cover_letters.txt")
        loader.save_processed_data(job_descriptions, "processed_job_descriptions.txt")
        
    except Exception as e:
        print(f"Error: {str(e)}")
