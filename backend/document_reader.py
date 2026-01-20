"""
Document Reader Module
Handles text extraction from various document formats (PDF, DOCX, TXT).
"""

import os
from typing import Optional
from pathlib import Path


def extract_text_from_document(file_path: str) -> str:
    """
    Extract text from various document formats.
    
    Args:
        file_path: Path to the document file
        
    Returns:
        Extracted text content
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Get file extension
    file_extension = file_path.suffix.lower()
    
    try:
        if file_extension == '.pdf':
            return extract_from_pdf(file_path)
        elif file_extension == '.docx':
            return extract_from_docx(file_path)
        elif file_extension == '.txt':
            return extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    except Exception as e:
        raise Exception(f"Error extracting text from {file_path}: {str(e)}")


def extract_from_pdf(file_path: str) -> str:
    """Extract text from PDF file."""
    try:
        import PyPDF2
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except ImportError:
        raise ImportError("PyPDF2 is required for PDF extraction. Install with: pip install PyPDF2")
    except Exception as e:
        raise Exception(f"Error reading PDF file: {str(e)}")


def extract_from_docx(file_path: str) -> str:
    """Extract text from DOCX file."""
    try:
        import docx
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except ImportError:
        raise ImportError("python-docx is required for DOCX extraction. Install with: pip install python-docx")
    except Exception as e:
        raise Exception(f"Error reading DOCX file: {str(e)}")


def extract_from_txt(file_path: str) -> str:
    """Extract text from TXT file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        raise Exception(f"Error reading TXT file: {str(e)}")


def is_supported_format(file_path: str) -> bool:
    """Check if file format is supported."""
    return Path(file_path).suffix.lower() in ['.pdf', '.docx', '.txt']


def get_file_info(file_path: str) -> dict:
    """Get information about a file."""
    file_path = Path(file_path)
    
    if not file_path.exists():
        return {'exists': False, 'error': 'File not found'}
    
    return {
        'exists': True,
        'extension': file_path.suffix,
        'size': file_path.stat().st_size if file_path.exists() else 0,
        'supported': is_supported_format(str(file_path))
    }
