# 🚀 Advanced Personalized Cover Letter Generator

An intelligent AI-powered cover letter generation system that creates truly unique, personalized cover letters based on resumes, job descriptions, and skills. Features dynamic template selection, advanced NLP processing, and maximum variety in output generation.

## ✨ Key Features

- **🎯 Dynamic Personalization**: Extracts name, experience, skills from resumes automatically
- **🔄 Maximum Variety**: 12+ template styles with randomization for unique output every time
- **🧠 Advanced NLP**: Smart job description parsing and skill categorization
- **📝 Multiple Input Methods**: Resume upload, JD upload, manual entry, skills-based
- **🎭 Dynamic Tone Adjustment**: Adapts style based on job role and experience level
- **🏢 Company Integration**: Personalizes content for specific companies
- **📊 Professional Output**: Clean, industry-standard formatting
- **🔧 Robust Error Handling**: Graceful fallbacks and user prompts

## 📁 Project Structure

```
personalized-cover-letter-generator/
├── backend/
│   ├── __init__.py                     # Package initialization
│   ├── generator.py                   # Core cover letter generation engine
│   ├── data_loader.py                 # Data loading utilities
│   ├── preprocessing.py               # Text preprocessing and cleaning
│   ├── vectorizer.py                  # TF-IDF vectorization
│   ├── similarity.py                  # Cosine similarity calculations
│   ├── matcher.py                    # Document matching logic
│   ├── main.py                       # Backend CLI interface
│   └── document_reader.py            # Multi-format document reading
├── sample_data/
│   └── cover_letter_data/             # Sample cover letters for reference
├── advanced_generator.py              # Main CLI application
├── requirements.txt                   # Python dependencies
└── README.md                        # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Quick Setup

1. **Navigate to project directory**:
   ```bash
   cd "C:\Users\Niladri\OneDrive\Desktop\AI-CL\personalized-cover-letter-generator"
   ```

2. **Install required packages**:
   ```bash
   pip install numpy pandas scikit-learn nltk PyPDF2 python-docx
   ```

3. **Download NLTK data** (first time only):
   ```python
   import nltk
   nltk.download('stopwords')
   nltk.download('wordnet')
   nltk.download('punkt')
   ```

4. **Run the application**:
   ```bash
   python advanced_generator.py
   ```

## 🚀 Quick Start Guide

### Running the Application

Simply execute the main script:
```bash
python advanced_generator.py
```

This will launch the interactive menu with 6 options:

### 📋 Menu Options

1. **📤 Upload Custom Job Description**
   - Upload JD file (PDF, DOCX, TXT)
   - Enter your details (name, experience, skills)
   - Enter company name (optional)
   - Generate personalized cover letter

2. **📁 Use Existing Job Description File**
   - Use pre-existing JD files from sample_data
   - Same personalization process

3. **✏️ Enter Job Description Manually**
   - Paste JD text directly
   - Quick generation without file upload

4. **📄 Resume-Based Generation** ⭐ **RECOMMENDED**
   - Upload resume file (PDF, DOCX, TXT)
   - Automatic extraction of name, experience, skills
   - Choose target position and company
   - Maximum personalization

5. **⚡ Skills-Based Generation**
   - Quick input of skills and experience
   - Fast generation for multiple applications

6. **🚪 Exit**
   - Exit the application

## 💡 Usage Examples

### Example 1: Resume-Based Generation (Most Popular)
```bash
python advanced_generator.py
# Choose option 4
# Upload resume: "C:\path\to\resume.pdf"
# Position: "Web Developer"
# Company: "TCS"
# Output: "my_cover_letter.txt"
```

### Example 2: Job Description Upload
```bash
python advanced_generator.py
# Choose option 1
# Upload JD: "C:\path\to\job_description.pdf"
# Enter: "John Doe, 5 years, python, java, sql"
# Company: "Amazon"
# Output: "amazon_cover_letter.txt"
```

### Example 3: Quick Skills-Based
```bash
python advanced_generator.py
# Choose option 5
# Enter: "Jane Smith, 3 years, react, nodejs, mongodb"
# Position: "Full Stack Developer"
# Company: "Google"
# Output: "google_dev_cover.txt"
```

## 🎯 Advanced Features

### Dynamic Template System
- **4 Fresher Templates**: Traditional, Modern, Direct, Story-based
- **4 Experienced Templates**: Professional, Results-driven, Impact-focused, Leadership
- **4 Mid-Level Templates**: Balanced, Growth-focused, Confident, Story-driven
- **Random Selection**: Different style every generation
- **300+ Unique Combinations**: Template × Opening × Closing × Skills

### Smart Content Generation
- **Skill Shuffling**: Different skill order each time
- **Tone Adaptation**: Professional, conversational, direct styles
- **Company Personalization**: Custom content for each company
- **Experience-Based Content**: Different for fresher vs experienced

### Robust Information Extraction
- **Name Detection**: Multiple patterns for various resume formats
- **Experience Parsing**: Years extraction with fallback prompts
- **Skill Categorization**: Programming, web, database, cloud, AI/ML
- **Achievement Recognition**: Project and accomplishment extraction

## 📊 Supported File Formats

### Input Formats
- **PDF**: `.pdf` files (resumes, job descriptions)
- **DOCX**: `.docx` files (Word documents)
- **TXT**: `.txt` files (plain text)

### Output Format
- **TXT**: Clean, professional text files
- **UTF-8 Encoding**: Universal character support
- **Proper Formatting**: Professional spacing and structure

## 🔧 Advanced Configuration

### Customizing Skills Database
Edit `backend/generator.py` to add new skills:
```python
self.skill_database = {
    'programming': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust'],
    'web': ['react', 'vue', 'angular', 'nodejs', 'express', 'django', 'flask', 'spring'],
    'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle'],
    'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'],
    'ai_ml': ['machine learning', 'tensorflow', 'pytorch', 'nlp', 'computer vision'],
    'tools': ['git', 'agile', 'scrum', 'jenkins', 'ci/cd', 'linux', 'windows']
}
```

### Adding Custom Templates
Add new templates in `backend/generator.py`:
```python
def _get_custom_templates(self) -> List[str]:
    return [
        """Custom template 1...""",
        """Custom template 2..."""
    ]
```

## 🐛 Troubleshooting

### Common Issues & Solutions

**Issue**: "ModuleNotFoundError"
```bash
# Solution: Install missing packages
pip install numpy pandas scikit-learn nltk PyPDF2 python-docx
```

**Issue**: "NLTK data not found"
```python
# Solution: Download NLTK data
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
```

**Issue**: "Name not detected"
- **Solution**: System will prompt for manual input
- Resume format varies, but fallback ensures functionality

**Issue**: "Experience not found"
- **Solution**: System asks for years of experience
- Enter manually when prompted

**Issue**: PDF reading errors
- **Solution**: Check file path and permissions
- Ensure PDF is not password-protected

## 🏆 Best Practices

### For Best Results
1. **Use Resume-Based Generation** (Option 4) for maximum personalization
2. **Provide accurate company names** for better customization
3. **Enter complete skill lists** for comprehensive matching
4. **Review generated letters** before sending
5. **Save different versions** for A/B testing

### File Organization
```
generated_cover_letters/
├── tcs_web_developer.txt
├── amazon_data_analyst.txt
├── google_ml_engineer.txt
└── microsoft_devops.txt
```

## 🤝 Team Collaboration

### For Team Members
1. **Clone the repository** to your local machine
2. **Follow setup instructions** above
3. **Run `python advanced_generator.py`** to start
4. **Choose option 4** for resume-based generation (recommended)
5. **Follow prompts** for personalized results

### Sharing Results
- Generated cover letters are saved as `.txt` files
- Easy to share via email, messaging, or version control
- Professional formatting maintained across all platforms

## 📞 Support & Contributing

### Getting Help
- Check this README first for common solutions
- Review troubleshooting section above
- Test with different resume formats if extraction fails

### Contributing
1. Fork the repository
2. Create feature branch
3. Add improvements or fixes
4. Test thoroughly
5. Submit pull request

## 📄 License

This project is licensed under MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- **NLTK**: Natural language processing tools
- **Scikit-learn**: Machine learning algorithms
- **Pandas**: Data manipulation
- **PyPDF2**: PDF reading capabilities
- **python-docx**: DOCX file processing
- **CoverPilot**: Inspiration for advanced features
- **AI-Powered Cover Letter Generator**: Template design patterns

---

**🚀 Ready to generate unique, personalized cover letters!**

**Team**: Advanced AI Development Team  
**Status**: Production Ready with Maximum Variety  
**Last Updated**: January 2026
