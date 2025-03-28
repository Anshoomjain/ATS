# ATS Resume Similarity Checker 🔍
**Automated resume scoring system for applicant tracking systems (ATS)**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![ATS Visualization](https://via.placeholder.com/800x400.png?text=ATS+Scoring+Process)

## Key Features ✨
- **PDF Resume Parsing**: Converts PDF resumes to text using OCR (Optical Character Recognition)
- **Job Description Analysis**: Processes job descriptions to identify key requirements
- **Context-Aware Filtering**:
  - Prioritizes relevant resume sections (Skills, Experience, Projects)
  - Ignores non-essential sections (Education, Hobbies)
- **Advanced Similarity Scoring**:
  - TF-IDF vectorization with cosine similarity
  - Keyword matching with synonym expansion
  - Hybrid scoring algorithm (75% keyword match, 25% contextual similarity)
- **NLP Preprocessing**:
  - Text normalization and stemming
  - Custom stopword removal
  - Punctuation/special character handling

## Installation 🛠️
### Prerequisites
- Python 3.8+
- Tesseract OCR (install via system package manager)
- Poppler-utils (for PDF conversion)

### Setup
1. Clone repository:
   ```
   git clone https://github.com/yourusername/ats-similarity-checker.git
   cd ats-similarity-checker
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install system dependencies:
   - **Windows**:
     ```
     choco install tesseract
     ```
   - **Ubuntu**:
     ```
     sudo apt-get install tesseract-ocr poppler-utils
     ```

## Usage 🚀
```
from ats_similarity import ATSSimilarityChecker, extract_text_from_pdf

# Initialize checker
checker = ATSSimilarityChecker()

# Example usage
resume_text = extract_text_from_pdf("resume.pdf")
job_description = "Seeking Python developer with ML experience..."

score = checker.calculate_similarity(job_description, resume_text)
print(f"ATS Match Score: {score}%")
```

## Configuration ⚙️
### Customization Options
```
# Modify relevant sections (in __init__ method)
self.relevant_sections = ["skills", "experience", "projects"]

# Adjust scoring weights
final_score = (tfidf_similarity * 0.25 + key_match_ratio * 0.75) * 100

# Add custom patterns for JD parsing
patterns = [
    r'\b(python|java|react|aws)\b'  # Add technology stack
]
```

## Dependencies 📦
| Package          | Version | Purpose                          |
|------------------|---------|----------------------------------|
| pdf2image        | 1.16.3  | PDF to image conversion          |
| pytesseract      | 0.3.10  | OCR text extraction              |
| scikit-learn     | 1.2.2   | TF-IDF vectorization             |
| nltk             | 3.8.1   | NLP preprocessing                |
| Pillow           | 9.5.0   | Image processing                 |

## Contributing 🤝
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/improvement`)
3. Commit changes with tests
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## License 📄
MIT License - See [LICENSE](LICENSE) for details

## Contact 📧
For support/questions:  
[![Email](https://img.shields.io/badge/Contact-Email%20Me-blue?logo=minutemailer)](mailto:your.email@example.com)
```

This README includes:
1. Clear feature breakdown
2. Installation instructions for different OS
3. Usage examples with code snippets
4. Configuration options
5. Dependency matrix
6. Contribution guidelines
7. Badges for visual appeal
8. Responsive formatting

You should:
1. Replace placeholder email/contact info
2. Add actual project URL in clone command
3. Add real visualization image URL
4. Update license if not using MIT
5. Add testing instructions if applicable
6. Include sample input/output files if needed

---
Answer from Perplexity: pplx.ai/share
