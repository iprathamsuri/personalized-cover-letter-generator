"""
Flask API for Advanced Cover Letter Generator
Web server for the cover letter generation application
"""

import os
import sys
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import random

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generator import CoverLetterGenerator
from document_reader import extract_text_from_document
from matcher import AdvancedMatcher
from similarity import SimilarityCalculator, ContentMatcher

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'temp'
app.config['JSON_SORT_KEYS'] = False

# Ensure temp directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the cover letter generator
generator = CoverLetterGenerator()

# Initialize advanced matcher and similarity calculator
matcher = AdvancedMatcher()
similarity_calculator = SimilarityCalculator()
content_matcher = ContentMatcher()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'doc'}

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    """Serve the homepage."""
    try:
        # Try to read and serve the home HTML file directly
        with open('templates/home.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add cache-busting meta tags and version
        content = content.replace('<head>', '<head>\n    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">\n    <meta http-equiv="Pragma" content="no-cache">\n    <meta http-equiv="Expires" content="0">\n    <meta name="version" content="2.0">')
        
        response = app.make_response(content)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response
    except Exception as e:
        print(f"Error serving homepage: {e}")
        return jsonify({'error': 'Homepage not found'}), 404

@app.route('/generator')
def generator_page():
    """Serve the generator interface."""
    try:
        # Try to read and serve the generator HTML file directly
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add cache-busting meta tags and version
        content = content.replace('<head>', '<head>\n    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">\n    <meta http-equiv="Pragma" content="no-cache">\n    <meta http-equiv="Expires" content="0">\n    <meta name="version" content="2.0">')
        
        response = app.make_response(content)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response
    except Exception as e:
        print(f"Error serving generator page: {e}")
        return jsonify({'error': 'Generator page not found'}), 404

@app.route('/api/info', methods=['GET'])
def get_info():
    """Get generator information."""
    return jsonify({
        'name': 'Advanced Cover Letter Generator',
        'version': '2.0',
        'description': 'AI-powered cover letter generation with advanced matching and similarity analysis',
        'features': [
            'Skills-based generation',
            'Resume-based generation',
            'Job description analysis',
            'Multiple templates',
            'Professional formatting',
            'Advanced matching analysis',
            'Resume-job compatibility analysis',
            'Similarity scoring',
            'Skill alignment assessment',
            'Tone appropriateness analysis'
        ],
        'methods': ['skills', 'resume', 'manual_jd'],
        'supported_formats': ['pdf', 'docx', 'txt'],
        'templates_available': {
            'fresher': len(generator._get_fresher_templates()),
            'experienced': len(generator._get_experienced_templates()),
            'mid_level': len(generator._get_mid_level_templates())
        },
        'analysis_features': {
            'matching_analysis': [
                'Overall score',
                'Content similarity',
                'Skill alignment',
                'Tone appropriateness',
                'Length appropriateness',
                'Keyword coverage',
                'Experience level match'
            ],
            'resume_analysis': [
                'Overall similarity',
                'Skill match percentage',
                'Experience match',
                'Missing skills identification',
                'Improvement recommendations'
            ],
            'similarity_metrics': [
                'Cosine similarity',
                'Jaccard similarity',
                'Combined similarity'
            ]
        },
        'endpoints': [
            'GET /api/info - Get generator information',
            'POST /api/generate - Generate cover letter with analysis',
            'POST /api/upload-resume - Upload resume file',
            'POST /api/upload-jd - Upload job description file',
            'POST /api/analyze-match - Analyze cover letter-job match',
            'POST /api/analyze-resume - Analyze resume-job compatibility'
        ],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/generate', methods=['POST'])
def generate_cover_letter():
    """Generate cover letter based on input method."""
    try:
        print("Generate endpoint called")
        data = request.get_json()
        print(f"🔍 Frontend Debug - Received data keys: {list(data.keys())}")
        print(f"🔍 Frontend Debug - Method: {data.get('method', 'N/A')}")
        print(f"🔍 Frontend Debug - User input length: {len(data.get('user_input', ''))}")
        print(f"🔍 Frontend Debug - User input preview: {data.get('user_input', '')[:100]}...")
        print(f"🔍 Frontend Debug - Target role: {data.get('target_role', 'N/A')}")
        print(f"🔍 Frontend Debug - Company: {data.get('company', 'N/A')}")
        print(f"🔍 Frontend Debug - Experience level: {data.get('experience_level', 'N/A')}")
        print(f"🔍 Frontend Debug - Job description length: {len(data.get('job_description', ''))}")
        print(f"🔍 Frontend Debug - Job description preview: {data.get('job_description', '')[:100]}...")
        
        # Extract required fields
        method = data.get('method', 'skills')
        user_input = data.get('user_input', '')
        job_description = data.get('job_description', '')
        target_role = data.get('target_role', 'Professional')
        company = data.get('company', '')
        resume_text = data.get('resume_text', '')
        experience_level = data.get('experience_level', 'mid-level')
        
        print(f"Method: {method}")
        print(f"User input length: {len(user_input)}")
        print(f"Resume text length: {len(resume_text)}")
        print(f"Experience level: {experience_level}")
        
        # Generate cover letter based on method
        if method == 'skills':
            if not user_input:
                return jsonify({'error': 'User input is required for skills-based generation'}), 400
            cover_letter = generator.generate_cover_letter(job_description, user_input, company=company, experience_level=experience_level, target_role=target_role)
            
        elif method == 'resume':
            if not resume_text and not user_input:
                return jsonify({'error': 'Resume text or user input is required for resume-based generation'}), 400
            # Use resume_text if available, otherwise use user_input
            input_text = resume_text or user_input
            cover_letter = generator.generate_cover_letter(job_description, input_text, company=company, experience_level=experience_level, target_role=target_role)
            
        elif method == 'manual_jd':
            if not job_description:
                return jsonify({'error': 'Job description is required for manual JD generation'}), 400
            if not user_input:
                return jsonify({'error': 'User input is required for manual JD generation'}), 400
            cover_letter = generator.generate_cover_letter(job_description, user_input, company=company, experience_level=experience_level, target_role=target_role)
            
        else:
            return jsonify({'error': 'Invalid generation method'}), 400
        
        # Perform matching analysis on generated cover letter
        matching_analysis = matcher.match_cover_letter_to_job(
            cover_letter, job_description, resume_text or user_input
        )
        
        print("Cover letter generated and analyzed successfully")
        
        return jsonify({
            'success': True,
            'cover_letter': cover_letter,
            'method': method,
            'timestamp': datetime.now().isoformat(),
            'generation_info': {
                'target_role': target_role,
                'company': company,
                'experience_level': experience_level,
                'word_count': len(cover_letter.split()),
                'character_count': len(cover_letter)
            },
            'matching_analysis': {
                'overall_score': round(matching_analysis['overall_score'], 3),
                'content_similarity': round(matching_analysis['content_similarity'], 3),
                'skill_alignment': round(matching_analysis['skill_alignment'], 3),
                'tone_appropriateness': round(matching_analysis['tone_appropriateness'], 3),
                'length_appropriateness': round(matching_analysis['length_appropriateness'], 3),
                'keyword_coverage': round(matching_analysis['keyword_coverage'], 3),
                'experience_level_match': round(matching_analysis['experience_level_match'], 3),
                'detailed_analysis': matching_analysis['detailed_analysis']
            }
        })
        
    except Exception as e:
        print(f"Error generating cover letter: {e}")
        return jsonify({'error': f'Generation failed: {str(e)}'}), 500

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    """Upload and extract text from resume file."""
    try:
        print("Resume upload endpoint called")
        
        if 'file' not in request.files:
            print("No file in request")
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        print(f"File received: {file.filename}")
        
        if file.filename == '':
            print("Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            print("Invalid file type")
            return jsonify({'error': 'File type not allowed. Please upload PDF, DOCX, or TXT files.'}), 400
        
        # Save temporary file
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        print(f"Saving file to: {temp_path}")
        file.save(temp_path)
        
        # Extract text
        print("Extracting text from document...")
        resume_text = extract_text_from_document(temp_path)
        print(f"Extracted text length: {len(resume_text)}")
        
        # Clean up
        os.remove(temp_path)
        print("Temporary file removed")
        
        if not resume_text.strip():
            return jsonify({'error': 'Could not extract text from the uploaded file'}), 400
        
        return jsonify({
            'success': True,
            'text': resume_text,
            'filename': file.filename,
            'word_count': len(resume_text.split()),
            'character_count': len(resume_text),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error uploading resume: {e}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/api/upload-jd', methods=['POST'])
def upload_jd():
    """Upload and extract text from job description file."""
    try:
        print("JD upload endpoint called")
        
        if 'file' not in request.files:
            print("No file in request")
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        print(f"File received: {file.filename}")
        
        if file.filename == '':
            print("Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            print("Invalid file type")
            return jsonify({'error': 'File type not allowed. Please upload PDF, DOCX, or TXT files.'}), 400
        
        # Save temporary file
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        print(f"Saving file to: {temp_path}")
        file.save(temp_path)
        
        # Extract text
        print("Extracting text from document...")
        jd_text = extract_text_from_document(temp_path)
        print(f"Extracted text length: {len(jd_text)}")
        
        # Clean up
        os.remove(temp_path)
        print("Temporary file removed")
        
        if not jd_text.strip():
            return jsonify({'error': 'Could not extract text from the uploaded file'}), 400
        
        return jsonify({
            'success': True,
            'text': jd_text,
            'filename': file.filename,
            'word_count': len(jd_text.split()),
            'character_count': len(jd_text),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error uploading job description: {e}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/api/analyze-match', methods=['POST'])
def analyze_match():
    """Analyze cover letter and job description match."""
    try:
        print("Match analysis endpoint called")
        data = request.get_json()
        
        # Extract required fields
        cover_letter = data.get('cover_letter', '')
        job_description = data.get('job_description', '')
        resume_text = data.get('resume_text', '')
        
        if not cover_letter:
            return jsonify({'error': 'Cover letter is required for match analysis'}), 400
        if not job_description:
            return jsonify({'error': 'Job description is required for match analysis'}), 400
        
        # Perform comprehensive matching analysis
        matching_analysis = matcher.match_cover_letter_to_job(
            cover_letter, job_description, resume_text
        )
        
        print("Match analysis completed successfully")
        
        return jsonify({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'matching_analysis': {
                'overall_score': round(matching_analysis['overall_score'], 3),
                'content_similarity': round(matching_analysis['content_similarity'], 3),
                'skill_alignment': round(matching_analysis['skill_alignment'], 3),
                'tone_appropriateness': round(matching_analysis['tone_appropriateness'], 3),
                'length_appropriateness': round(matching_analysis['length_appropriateness'], 3),
                'keyword_coverage': round(matching_analysis['keyword_coverage'], 3),
                'experience_level_match': round(matching_analysis['experience_level_match'], 3),
                'detailed_analysis': matching_analysis['detailed_analysis']
            },
            'analysis_info': {
                'cover_letter_word_count': len(cover_letter.split()),
                'job_description_word_count': len(job_description.split()),
                'resume_provided': bool(resume_text),
                'resume_word_count': len(resume_text.split()) if resume_text else 0
            }
        })
        
    except Exception as e:
        print(f"Error analyzing match: {e}")
        return jsonify({'error': f'Match analysis failed: {str(e)}'}), 500

@app.route('/api/analyze-resume', methods=['POST'])
def analyze_resume():
    """Analyze resume and job description compatibility."""
    try:
        print("Resume analysis endpoint called")
        data = request.get_json()
        
        # Extract required fields
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        
        if not resume_text:
            return jsonify({'error': 'Resume text is required for resume analysis'}), 400
        if not job_description:
            return jsonify({'error': 'Job description is required for resume analysis'}), 400
        
        # Perform resume-job matching
        resume_match = content_matcher.match_resume_to_job(resume_text, job_description)
        
        # Get improvement recommendations
        recommendations = content_matcher.recommend_improvements(resume_text, job_description)
        
        # Calculate similarity scores
        similarity_scores = {
            'cosine_similarity': similarity_calculator.cosine_similarity(resume_text, job_description),
            'jaccard_similarity': similarity_calculator.jaccard_similarity(resume_text, job_description),
            'combined_similarity': similarity_calculator.combined_similarity(resume_text, job_description)
        }
        
        print("Resume analysis completed successfully")
        
        return jsonify({
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'resume_match': {
                'overall_similarity': round(resume_match['overall_similarity'], 3),
                'skill_match': round(resume_match['skill_match'], 3),
                'experience_match': round(resume_match['experience_match'], 3),
                'matched_skills': resume_match['matched_skills'],
                'missing_skills': resume_match['missing_skills'],
                'resume_skills': resume_match['resume_skills'],
                'required_skills': resume_match['required_skills']
            },
            'similarity_scores': {
                'cosine_similarity': round(similarity_scores['cosine_similarity'], 3),
                'jaccard_similarity': round(similarity_scores['jaccard_similarity'], 3),
                'combined_similarity': round(similarity_scores['combined_similarity'], 3)
            },
            'recommendations': recommendations,
            'analysis_info': {
                'resume_word_count': len(resume_text.split()),
                'job_description_word_count': len(job_description.split()),
                'total_matched_skills': len(resume_match['matched_skills']),
                'total_missing_skills': len(resume_match['missing_skills']),
                'skill_match_percentage': round(resume_match['skill_match'] * 100, 1)
            }
        })
        
    except Exception as e:
        print(f"Error analyzing resume: {e}")
        return jsonify({'error': f'Resume analysis failed: {str(e)}'}), 500

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """Test endpoint to verify server is working."""
    return jsonify({
        'status': 'Server is running',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0',
        'endpoints': [
            'GET /api/info - Get generator information',
            'POST /api/generate - Generate cover letter',
            'POST /api/upload-resume - Upload resume file',
            'POST /api/upload-jd - Upload job description file',
            'POST /api/analyze-match - Analyze cover letter-job match',
            'POST /api/analyze-resume - Analyze resume-job compatibility'
        ]
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(413)
def too_large(error):
    """Handle file too large errors."""
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

if __name__ == '__main__':
    print("🚀 Starting Advanced Cover Letter Generator Web Server...")
    print("📱 Server will be available at: http://localhost:5000")
    print("🌐 API endpoints:")
    print("   GET  /api/info - Get generator information")
    print("   POST /api/generate - Generate cover letter")
    print("   POST /api/upload-resume - Upload resume file")
    print("   POST /api/upload-jd - Upload job description file")
    print("   POST /api/analyze-match - Analyze cover letter-job match")
    print("   POST /api/analyze-resume - Analyze resume-job compatibility")
    print()
    
    # Change to the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    sys.path.insert(0, project_root)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
