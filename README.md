# Personalized Cover Letter Generator (AI)

A platform-independent Python application that matches cover letters to job descriptions using TF-IDF vectorization and cosine similarity analysis. This tool helps job seekers find the most suitable cover letters for specific job descriptions and provides detailed matching insights.

## 🚀 Features

- **Smart Matching**: Uses TF-IDF vectorization and cosine similarity to find best matches
- **Text Preprocessing**: Advanced text cleaning with stopword removal and lemmatization
- **Keyword Extraction**: Identifies important keywords from cover letters and job descriptions
- **Similarity Analysis**: Provides detailed similarity scores and match reports
- **Command-line Interface**: Easy-to-use CLI with multiple operation modes
- **Interactive Mode**: User-friendly interactive exploration mode
- **Export Functionality**: Export results to CSV for further analysis

## 📁 Project Structure

```
personalized-cover-letter-generator/
│
├── sample_data/
│   ├── cover_letter_data/
│   │   └── cover_letters.txt          # Sample cover letter dataset
│   └── job_description_data/
│       └── job_descriptions.txt      # Sample job description dataset
│
├── backend/
│   ├── data_loader.py                # Data loading and parsing
│   ├── preprocessing.py              # Text preprocessing and cleaning
│   ├── vectorizer.py                 # TF-IDF vectorization
│   ├── similarity.py                 # Cosine similarity calculations
│   ├── matcher.py                    # Main matching logic
│   └── main.py                       # CLI entry point
│
├── LICENSE
└── README.md
```

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. **Clone or download the project**:
   ```bash
   cd personalized-cover-letter-generator
   ```

2. **Install required packages**:
   ```bash
   pip install numpy pandas scikit-learn nltk
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
   python backend/main.py --help
   ```

## 📊 Usage

### Command Line Interface

The application provides several command-line options:

#### 1. Run Complete Pipeline
```bash
python backend/main.py pipeline [--cl-file COVER_LETTER_FILE] [--jd-file JOB_DESCRIPTION_FILE] [--method basic|advanced] [--export OUTPUT_FILE]
```

Example:
```bash
python backend/main.py pipeline --export matches.csv
```

#### 2. Find Matches for Specific Job Description
```bash
python backend/main.py match JD_INDEX [--top-n N]
```

Example:
```bash
python backend/main.py match 0 --top-n 5
```

#### 3. Analyze Data Statistics
```bash
python backend/main.py analyze --type cover_letters|job_descriptions|all
```

Example:
```bash
python backend/main.py analyze --type all
```

#### 4. Extract Keywords
```bash
python backend/main.py keywords --type cover_letters|job_descriptions [--top-n N]
```

Example:
```bash
python backend/main.py keywords --type cover_letters --top-n 20
```

#### 5. Interactive Mode
```bash
python backend/main.py interactive
```

In interactive mode, you can use:
- `help` - Show available commands
- `match <jd_index>` - Find matches for job description
- `stats` - Show data statistics
- `top` - Show top overall matches
- `keywords <type>` - Show keywords
- `quit` - Exit

### Python API Usage

```python
from backend.matcher import CoverLetterMatcher

# Initialize matcher
matcher = CoverLetterMatcher()

# Run complete pipeline
matcher.run_full_pipeline()

# Find best matches for job description 0
matches = matcher.find_best_matches(0, top_n=3)
for cl_idx, score in matches:
    print(f"Cover Letter {cl_idx}: {score:.4f}")

# Get detailed match report
report = matcher.get_match_report(0, 0)
print(f"Similarity: {report['similarity_score']:.4f}")
```

## 📈 How It Works

1. **Data Loading**: Loads cover letters and job descriptions from text files
2. **Text Preprocessing**: Cleans and normalizes text using NLP techniques
3. **Vectorization**: Converts text to TF-IDF vectors for numerical analysis
4. **Similarity Calculation**: Computes cosine similarity between documents
5. **Matching**: Finds best matches based on similarity scores
6. **Reporting**: Provides detailed match reports and insights

## 📋 Data Format

### Cover Letter Format
Text files with documents separated by underscores (`__________`):

```
📁 COVER LETTER DATASET
________________________________________
🔹 Cover Letter Sample 1
[Cover letter text here]
________________________________________
🔹 Cover Letter Sample 2
[Cover letter text here]
```

### Job Description Format
Similar structure with job descriptions:

```
📁 JOB DESCRIPTION DATASET
________________________________________
🔹 Job Description Sample 1
[Job description text here]
```

## 🔧 Configuration

### Customizing Preprocessing
```python
from backend.preprocessing import TextPreprocessor

preprocessor = TextPreprocessor()
cleaned_text = preprocessor.clean_text_advanced(raw_text)
```

### Adjusting Vectorization
```python
from backend.vectorizer import TFIDFVectorizer

vectorizer = TFIDFVectorizer(max_features=10000, stop_words='english')
```

## 📊 Output Examples

### Similarity Scores
```
Top 5 matches for Job Description 0:
1. Cover Letter 0: 0.8234
2. Cover Letter 2: 0.7456
3. Cover Letter 1: 0.6789
```

### Keywords
```
Top 10 Keywords for Cover Letters:
1. experience        0.2345
2. development      0.1987
3. python          0.1765
4. software        0.1543
5. developer       0.1432
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- NLTK for natural language processing tools
- Scikit-learn for machine learning algorithms
- Pandas for data manipulation
- Reference projects: CoverPilot and AI-Powered Cover Letter Generator

## 📞 Support

For questions or issues, please open an issue on the repository or contact the development team.

---

**Team**: Group 1 – Infosys Springboard Internship (Batch 11)  
**Status**: Development Phase - Platform-independent implementation completed
