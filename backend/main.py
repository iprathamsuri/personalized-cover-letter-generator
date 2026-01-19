"""
Main Entry Point
Command-line interface for the personalized cover letter generator.
"""

import argparse
import sys
import os
from pathlib import Path

# Add backend directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from matcher import CoverLetterMatcher
from data_loader import DataLoader
from preprocessing import TextPreprocessor
from vectorizer import TFIDFVectorizer
from similarity import SimilarityCalculator
from generator import CoverLetterGenerator


def main():
    """Main function to handle command-line arguments and run the application."""
    parser = argparse.ArgumentParser(
        description="Personalized Cover Letter Generator - Match cover letters to job descriptions"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Full pipeline command
    pipeline_parser = subparsers.add_parser('pipeline', help='Run the complete matching pipeline')
    pipeline_parser.add_argument('--cl-file', type=str, help='Specific cover letter file')
    pipeline_parser.add_argument('--jd-file', type=str, help='Specific job description file')
    pipeline_parser.add_argument('--method', type=str, default='advanced', 
                                choices=['basic', 'advanced'], help='Preprocessing method')
    pipeline_parser.add_argument('--export', type=str, help='Export matches to CSV file')
    
    # Match specific job description
    match_parser = subparsers.add_parser('match', help='Find matches for a specific job description')
    match_parser.add_argument('jd_index', type=int, help='Job description index')
    match_parser.add_argument('--top-n', type=int, default=3, help='Number of top matches to return')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze data and show statistics')
    analyze_parser.add_argument('--type', type=str, required=True,
                               choices=['cover_letters', 'job_descriptions', 'all'],
                               help='Type of data to analyze')
    
    # Keywords command
    keywords_parser = subparsers.add_parser('keywords', help='Extract top keywords from documents')
    keywords_parser.add_argument('--type', type=str, required=True,
                                 choices=['cover_letters', 'job_descriptions'],
                                 help='Document type for keyword extraction')
    keywords_parser.add_argument('--top-n', type=int, default=20, help='Number of keywords to extract')
    
    # Interactive mode
    interactive_parser = subparsers.add_parser('interactive', help='Run in interactive mode')

    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate personalized cover letter')
    generate_parser.add_argument('--jd-file', type=str, help='Job description file path')
    generate_parser.add_argument('--user-input', type=str, help='User skills and experience input')
    generate_parser.add_argument('--use-match', type=int, help='Use best match index for content')
    generate_parser.add_argument('--output', type=str, help='Output file for generated cover letter')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize matcher
    matcher = CoverLetterMatcher()
    
    try:
        if args.command == 'pipeline':
            run_pipeline(matcher, args)
        elif args.command == 'match':
            run_match(matcher, args)
        elif args.command == 'analyze':
            run_analysis(matcher, args)
        elif args.command == 'keywords':
            run_keywords(matcher, args)
        elif args.command == 'interactive':
            run_interactive_mode(matcher)
        elif args.command == 'generate':
            run_generate(matcher, args)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def run_pipeline(matcher, args):
    """Run the complete matching pipeline."""
    print("🚀 Starting Cover Letter Matching Pipeline")
    print("=" * 50)
    
    # Run full pipeline
    matcher.run_full_pipeline(
        cover_letter_file=args.cl_file,
        job_description_file=args.jd_file,
        preprocessing_method=args.method
    )
    
    # Show top matches
    print("\n📊 Top 10 Overall Matches:")
    print("-" * 30)
    top_matches = matcher.get_top_matches_overall(10)
    for i, (cl_idx, jd_idx, score) in enumerate(top_matches, 1):
        print(f"{i:2d}. Cover Letter {cl_idx:2d} - Job Description {jd_idx:2d}: {score:.4f}")
    
    # Export if requested
    if args.export:
        matcher.export_matches_to_csv(args.export, top_n=50)
    
    print("\n✅ Pipeline completed successfully!")


def run_match(matcher, args):
    """Find matches for a specific job description."""
    print(f"\nTop 5 matches for Job Description {args.jd_index}:")
    print("=" * 50)
    
    # Run pipeline if not already done
    if matcher.similarity_matrix is None:
        print("Running pipeline first...")
        matcher.run_full_pipeline()
    
    # Find matches
    matches = matcher.find_best_matches(args.jd_index, top_n=args.top_n)
    
    print(f"\n📋 Top {args.top_n} Cover Letter Matches:")
    print("-" * 40)
    for i, (cl_idx, score) in enumerate(matches, 1):
        print(f"{i}. Cover Letter {cl_idx}: {score:.4f}")
        
        # Show preview
        preview = matcher.cover_letters[cl_idx][:150] + "..."
        print(f"   Preview: {preview}")
        print()
    
    # Show detailed report for top match
    if matches:
        top_cl_idx, top_score = matches[0]
        print(f"\nDetailed Report for Top Match:")
        print("-" * 40)
        report = matcher.get_match_report(top_cl_idx, args.jd_index)
        print(f"Similarity Score: {report['similarity_score']:.4f}")
        print(f"Cover Letter Keywords: {[kw for kw, _ in report['cover_letter_keywords'][:5]]}")
        print(f"Job Description Keywords: {[kw for kw, _ in report['job_description_keywords'][:5]]}")


def run_analysis(matcher, args):
    """Analyze data and show statistics."""
    print(f"📊 Analyzing {args.type.replace('_', ' ').title()}")
    print("=" * 50)
    
    # Load data
    matcher.load_data()
    matcher.preprocess_data()
    
    preprocessor = matcher.preprocessor
    
    if args.type == 'cover_letters':
        docs = matcher.processed_cover_letters
        raw_docs = matcher.cover_letters
    elif args.type == 'job_descriptions':
        docs = matcher.processed_job_descriptions
        raw_docs = matcher.job_descriptions
    else:  # all
        docs = matcher.processed_cover_letters + matcher.processed_job_descriptions
        raw_docs = matcher.cover_letters + matcher.job_descriptions
    
    # Get statistics
    stats = preprocessor.get_text_statistics(docs)
    
    print(f"📈 Data Statistics:")
    print(f"   Total Documents: {stats['total_documents']}")
    print(f"   Total Words: {stats['total_words']}")
    print(f"   Average Words per Document: {stats['average_words_per_document']:.1f}")
    print(f"   Unique Vocabulary Size: {stats['unique_vocabulary_size']}")
    
    # Document length distribution
    lengths = [len(doc.split()) for doc in docs]
    print(f"\n📏 Document Length Distribution:")
    print(f"   Min Length: {min(lengths)} words")
    print(f"   Max Length: {max(lengths)} words")
    print(f"   Median Length: {sorted(lengths)[len(lengths)//2]} words")


def run_generate(matcher, args):
    """Generate personalized cover letter."""
    print("📝 Generating Personalized Cover Letter")
    print("=" * 50)
    
    # Initialize generator
    generator = CoverLetterGenerator()
    
    # Load job description
    if args.jd_file:
        with open(args.jd_file, 'r', encoding='utf-8') as f:
            job_description = f.read()
    else:
        job_description = input("Enter job description: ")
    
    # Load user input
    if args.user_input:
        user_input = args.user_input
    else:
        user_input = input("Enter your skills and experience (e.g., 'My name is John and I have 3 years of experience in Python...'): ")
    
    # Get best match content if requested
    best_match_content = ""
    if args.use_match is not None:
        # Run pipeline first to get matches
        if matcher.similarity_matrix is None:
            print("Loading data for matching...")
            matcher.run_full_pipeline()
        
        # Get best match
        matches = matcher.find_best_matches(args.use_match, top_n=1)
        if matches:
            best_match_content = matcher.cover_letters[matches[0][0]][:500]
    
    # Generate cover letter
    cover_letter = generator.generate_cover_letter(
        job_description=job_description,
        user_input=user_input,
        best_match_content=best_match_content
    )
    
    # Save or display output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(cover_letter)
        print(f"\n✅ Cover letter saved to: {args.output}")
    else:
        print("\n📄 Generated Cover Letter:")
        print("=" * 50)
        print(cover_letter)
    
    print("\n🎯 Generation Info:")
    try:
        print(generator.get_generation_info())
    except AttributeError as e:
        print(f"Generation completed with available features: {generator.get_generation_info()}")
    """Extract and display top keywords."""
    print(f"🔤 Extracting Top {args.top_n} Keywords from {args.type.replace('_', ' ').title()}")
    print("=" * 60)
    
    # Load and process data
    matcher.load_data()
    matcher.preprocess_data()
    matcher.vectorize_data()
    
    # Get keywords
    if args.type == 'cover_letters':
        # Get keywords from cover letters only
        cl_vectors = matcher.cover_letter_vectors
        vectorizer = matcher.vectorizer
        
        # Create temporary vectorizer for just cover letters
        temp_vectorizer = TFIDFVectorizer()
        temp_vectorizer.vectorizer = vectorizer.vectorizer
        temp_vectorizer.feature_names = vectorizer.feature_names
        temp_vectorizer.tfidf_matrix = cl_vectors
        
        keywords_df = temp_vectorizer.get_top_keywords(args.top_n)
    else:  # job_descriptions
        # Get keywords from job descriptions only
        jd_vectors = matcher.job_description_vectors
        vectorizer = matcher.vectorizer
        
        # Create temporary vectorizer for just job descriptions
        temp_vectorizer = TFIDFVectorizer()
        temp_vectorizer.vectorizer = vectorizer.vectorizer
        temp_vectorizer.feature_names = vectorizer.feature_names
        temp_vectorizer.tfidf_matrix = jd_vectors
        
        keywords_df = temp_vectorizer.get_top_keywords(args.top_n)
    
    print(f"📋 Top {args.top_n} Keywords:")
    print("-" * 30)
    for i, row in keywords_df.iterrows():
        print(f"{i+1:2d}. {row['Keyword']:<20} {row['Importance']:.4f}")


def run_interactive_mode(matcher):
    """Run the application in interactive mode."""
    print("Interactive Mode")
    print("=" * 30)
    print("Type 'help' for available commands or 'quit' to exit.")
    
    # Run pipeline first
    print("Initializing data...")
    try:
        matcher.run_full_pipeline()
        print("Data loaded and processed successfully!")
    except Exception as e:
        print(f"Error initializing data: {str(e)}")
        print("Please make sure you have data files in the sample_data directories.")
        return
    
    while True:
        try:
            try:
                command = input("\n> ").strip().lower()
            except EOFError:
                print("\nGoodbye!")
                break
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            
            if command == 'quit' or command == 'exit':
                print("👋 Goodbye!")
                break
            elif command == 'help':
                print_help()
            elif command.startswith('match '):
                try:
                    jd_index = int(command.split()[1])
                    show_interactive_matches(matcher, jd_index)
                except (ValueError, IndexError):
                    print("❌ Usage: match <job_description_index>")
            elif command == 'stats':
                show_interactive_stats(matcher)
            elif command == 'top':
                show_interactive_top_matches(matcher)
            elif command.startswith('keywords '):
                try:
                    doc_type = command.split()[1]
                    show_interactive_keywords(matcher, doc_type)
                except IndexError:
                    print("❌ Usage: keywords <cover_letters|job_descriptions>")
            else:
                print("Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")


def print_help():
    """Print help for interactive mode."""
    print("\nAvailable Commands:")
    print("  help                           - Show this help message")
    print("  match <jd_index>              - Find matches for job description")
    print("  stats                         - Show data statistics")
    print("  top                           - Show top 10 overall matches")
    print("  keywords <type>               - Show keywords (cover_letters/job_descriptions)")
    print("  generate                       - Generate personalized cover letter")
    print("  quit/exit                     - Exit interactive mode")


def show_interactive_matches(matcher, jd_index):
    """Show matches in interactive mode."""
    try:
        matches = matcher.find_best_matches(jd_index, top_n=5)
        print(f"\n🔍 Top 5 matches for Job Description {jd_index}:")
        for i, (cl_idx, score) in enumerate(matches, 1):
            print(f"{i}. Cover Letter {cl_idx}: {score:.4f}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def show_interactive_stats(matcher):
    """Show statistics in interactive mode."""
    print(f"\nData Statistics:")
    print(f"   Cover Letters: {len(matcher.cover_letters)}")
    print(f"   Job Descriptions: {len(matcher.job_descriptions)}")
    print(f"   Vocabulary Size: {matcher.vectorizer.get_vocabulary_size()}")
    
    if matcher.similarity_matrix is not None:
        stats = matcher.similarity_calculator.get_similarity_statistics()
        print(f"   Average Similarity: {stats.get('mean_similarity', 0):.4f}")


def show_interactive_top_matches(matcher):
    """Show top matches in interactive mode."""
    top_matches = matcher.get_top_matches_overall(10)
    print(f"\nTop 10 Overall Matches:")
    for i, (cl_idx, jd_idx, score) in enumerate(top_matches, 1):
        print(f"{i:2d}. Cover Letter {cl_idx:2d} - Job Description {jd_idx:2d}: {score:.4f}")


def show_interactive_keywords(matcher, doc_type):
    """Show keywords in interactive mode."""
    try:
        if doc_type == 'cover_letters':
            vectors = matcher.cover_letter_vectors
        elif doc_type == 'job_descriptions':
            vectors = matcher.job_description_vectors
        else:
            print("Type must be 'cover_letters' or 'job_descriptions'")
            return
        
        # Create temporary vectorizer
        temp_vectorizer = TFIDFVectorizer()
        temp_vectorizer.vectorizer = matcher.vectorizer.vectorizer
        temp_vectorizer.feature_names = matcher.vectorizer.feature_names
        temp_vectorizer.tfidf_matrix = vectors
        
        keywords_df = temp_vectorizer.get_top_keywords(10)
        print(f"\nTop 10 Keywords for {doc_type.replace('_', ' ').title()}:")
        for i, row in keywords_df.iterrows():
            print(f"{i+1:2d}. {row['Keyword']:<20} {row['Importance']:.4f}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
