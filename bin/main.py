"""
Main CLI Interface for the Personalized Cover Letter Generator.
Handles command-line arguments and orchestrates the NLP pipeline.
"""

import argparse
import sys
from typing import List
from .data_loader import DataLoader
from .preprocessing import TextPreprocessor
from .vectorizer import TFIDFVectorizer
from .similarity import SimilarityCalculator
from .matcher import CoverLetterMatcher
from .generator import CoverLetterGenerator


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description='Personalized Cover Letter Generator with NLP Matching',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Add arguments
    parser.add_argument(
        'command',
        choices=['pipeline', 'match', 'analyze', 'keywords', 'interactive', 'generate'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--cover-letters',
        type=str,
        default=None,
        help='Path to cover letters directory'
    )
    
    parser.add_argument(
        '--job-descriptions',
        type=str,
        default=None,
        help='Path to job descriptions directory'
    )
    
    parser.add_argument(
        '--top-n',
        type=int,
        default=5,
        help='Number of top matches to return'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output file for results'
    )
    
    return parser


def print_help():
    """Print help information."""
    print("""
Available Commands:
================

1. pipeline - Run the complete NLP pipeline
2. match     - Match cover letters to job descriptions
3. analyze   - Analyze job descriptions and cover letters
4. keywords  - Extract keywords from documents
5. interactive - Interactive cover letter generation
6. generate  - Generate personalized cover letters

Examples:
---------
python main.py pipeline
python main.py match --top-n 3
python main.py interactive
python main.py generate --job-descriptions ./jds --cover-letters ./cls --output matches.txt
    """)


def run_pipeline(args):
    """Run the complete NLP pipeline."""
    print("🔄 Running NLP Pipeline...")
    
    # Initialize components
    matcher = CoverLetterMatcher(
        cover_letter_dir=args.cover_letters,
        job_description_dir=args.job_descriptions
    )
    
    # Get matching info
    matching_info = matcher.get_matching_info(
        job_description="sample job description",
        top_n=args.top_n
    )
    
    print(f"✅ Pipeline completed successfully!")
    print(f"📊 Processed {matching_info['total_cover_letters']} cover letters")
    print(f"📊 Processed {matching_info['total_job_descriptions']} job descriptions")
    print(f"🎯 Top {matching_info['top_n']} matches ready for analysis")


def run_match(args):
    """Run matching between cover letters and job descriptions."""
    print("🔍 Matching cover letters to job descriptions...")
    
    # Initialize matcher
    matcher = CoverLetterMatcher(
        cover_letter_dir=args.cover_letters,
        job_description_dir=args.job_descriptions
    )
    
    # Get matches
    matches = matcher.match_cover_letter_to_job_description(
        job_description="sample job description",
        top_n=args.top_n
    )
    
    print(f"✅ Found {len(matches)} matches:")
    for i, (idx, similarity) in enumerate(matches):
        print(f"  {i+1}. Cover Letter {idx} - Similarity: {similarity:.3f}")
    
    return matches


def run_analyze(args):
    """Run analysis on documents."""
    print("📊 Analyzing documents...")
    
    # Initialize components
    matcher = CoverLetterMatcher(
        cover_letter_dir=args.cover_letters,
        job_description_dir=args.job_descriptions
    )
    
    # Get statistics
    matching_info = matcher.get_matching_info(
        job_description="sample job description",
        top_n=args.top_n
    )
    
    print(f"✅ Analysis completed!")
    print(f"📊 Total cover letters: {matching_info['total_cover_letters']}")
    print(f"📊 Total job descriptions: {matching_info['total_job_descriptions']}")
    print(f"📊 Vocabulary size: {matcher.get_vocabulary_size()}")


def run_keywords(args):
    """Extract keywords from documents."""
    print("🔑 Extracting keywords...")
    
    # Initialize components
    matcher = CoverLetterMatcher(
        cover_letter_dir=args.cover_letters,
        job_description_dir=args.job_descriptions
    )
    
    # Get top keywords
    matches = matcher.match_cover_letter_to_job_description(
        job_description="sample job description",
        top_n=args.top_n
    )
    
    print(f"✅ Top {len(matches)} keywords:")
    for i, (idx, similarity) in enumerate(matches):
        print(f"  {i+1}. {matcher.feature_names[idx]} - Score: {similarity:.3f}")


def run_interactive(args):
    """Run interactive cover letter generation."""
    print("🎯 Starting interactive generation...")
    
    generator = CoverLetterGenerator()
    
    # Get user input
    user_input = input("📝 Enter your details (name, experience, skills): ").strip()
    
    # Generate cover letter
    cover_letter = generator.generate_cover_letter(
        job_description="We are looking for a Software Developer with experience in Python and JavaScript.",
        user_input=user_input
    )
    
    print(f"✅ Cover letter generated successfully!")
    print(f"📄 Generated Cover Letter:")
    print("=" * 50)
    print(cover_letter)


def run_generate(args):
    """Generate personalized cover letters."""
    print("🚀 Generating personalized cover letters...")
    
    generator = CoverLetterGenerator()
    
    # Initialize matcher for best matches
    matcher = CoverLetterMatcher(
        cover_letter_dir=args.cover_letters,
        job_description_dir=args.job_descriptions
    )
    
    # Generate cover letters for each job description
    for i, job_desc in enumerate(matcher.job_descriptions):
        best_match_content = matcher.get_best_match_content(job_desc, top_n=3)
        
        cover_letter = generator.generate_cover_letter(
            job_description=job_desc,
            user_input="My name is John Doe and I have 3 years of experience in Python, Django, and React."
        )
        
        print(f"✅ Generated cover letter {i+1}")
        print("=" * 50)
        print(cover_letter)


def print_help():
    """Print help information."""
    print("""
Available Commands:
================

1. pipeline - Run the complete NLP pipeline
2. match     - Match cover letters to job descriptions
3. analyze   - Analyze job descriptions and cover letters
4. keywords  - Extract keywords from documents
5. interactive - Interactive cover letter generation
6. generate  - Generate personalized cover letters

Examples:
---------
python main.py pipeline
python main.py match --top-n 3
python main.py interactive
python main.py generate --job-descriptions ./jds --cover-letters ./cls --output matches.txt
    """)


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if args.command == 'pipeline':
        run_pipeline(args)
    elif args.command == 'match':
        run_match(args)
    elif args.command == 'analyze':
        run_analyze(args)
    elif args.command == 'keywords':
        run_keywords(args)
    elif args.command == 'interactive':
        run_interactive(args)
    elif args.command == 'generate':
        run_generate(args)
    else:
        print_help()


if __name__ == "__main__":
    main()
