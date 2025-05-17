# Resume Parser Project

A sophisticated resume parsing system that uses Natural Language Processing (NLP) and machine learning techniques to extract, analyze, and structure information from resumes in various formats (PDF, DOCX, TXT).

## Features

- **Multi-format Support**: Handles PDF, DOCX, and text-based resumes
- **Advanced Entity Extraction**:
  - Personal Information (Name, Email, Phone)
  - Professional Links (GitHub, LinkedIn)
  - Skills and Technologies
  - Education History
- **Skills Analysis**:
  - Automated skill extraction
  - Skill matching against job descriptions
  - Missing skills identification
- **Resume Ranking**:
  - Skill-based matching score
  - Semantic similarity analysis
  - Weighted scoring system
- **Output Formats**:
  - JSON detailed results
  - CSV summary reports
  - Interactive HTML reports
  - Terminal-friendly output

## Project Structure

```
resume-parser/
├── data/
│   ├── job_description.txt         # Job requirements/description
│   ├── skills.txt                  # Dictionary of technical skills
│   ├── output.txt                  # Parser output for single resume
│   └── resumes/                    # Directory for resume PDFs
├── src/
│   ├── entity_extractor.py         # Extracts entities (name, email, etc.)
│   ├── experience_extractor.py     # Analyzes work experience sections
│   ├── skill_extractor.py         # Extracts technical skills
│   ├── input_handler.py           # Handles different file formats
│   ├── job_skills_extractor.py    # Extracts skills from job descriptions
│   ├── section_segmenter.py       # Segments resume into sections
│   ├── resume_parser_main.py      # Main parser entry point
│   ├── resume_ranking_pipeline.py # Resume ranking system
│   └── resume_job_matcher.py      # Matches resumes to job descriptions
├── output/
│   ├── ranked_resumes.json        # Detailed ranking results
│   ├── resume_ranking_report.html # Visual HTML report
│   └── resume_ranking_summary.csv # Summary of rankings
├── test/                          # Unit tests
│   └── ...
├── requirements.txt               # Project dependencies
└── README.md                     # Project documentation
```

## Technologies Used

- **Python 3.8+**
- **Core Libraries**:
  - PyPDF2: PDF parsing
  - pandas: Data manipulation
  - numpy: Numerical operations
  - scikit-learn: Text processing and similarity calculations
- **NLP & Text Processing**:
  - NLTK: Natural language processing
  - spaCy: Entity recognition
  - regex: Pattern matching

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/resume-parser.git
cd resume-parser
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Resume Parsing

```python
from resume_parser_main import parse_resume

# Parse a single resume
result = parse_resume("path/to/resume.pdf")
print(result)
```

### Resume Ranking Pipeline

```python
from resume_ranking_pipeline import main as rank_resumes

# Rank multiple resumes against a job description
rank_resumes()
```

### Command Line Interface

```bash
# Parse a single resume
python resume_parser_main.py --input "path/to/resume.pdf" --output "output.json"

# Rank multiple resumes
python resume_ranking_pipeline.py --job "job_description.txt" --resumes "resumes_directory/"
```

## Output Format

The parser generates multiple output formats:

### JSON Output

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "skills": ["python", "java", "machine learning"],
  "education": ["BS Computer Science"],
  "github": "https://github.com/johndoe",
  "linkedin": "https://linkedin.com/in/johndoe"
}
```

### Ranking Results

- HTML report with interactive visualization
- CSV summary with ranking scores
- Detailed JSON with skill matches and scores

## Key Components

- **Entity Extractor**: Extracts personal information and contact details
- **Skill Extractor**: Identifies technical and soft skills using NLP
- **Experience Analyzer**: Processes work experience sections
- **Job Skills Extractor**: Analyzes job requirements
- **Resume Ranking Pipeline**: Ranks resumes based on multiple criteria
- **Resume-Job Matcher**: Matches resumes to job descriptions

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Requirements

Create a `requirements.txt` file with:

```
PyPDF2>=3.0.0
pandas>=1.3.0
numpy>=1.20.0
scikit-learn>=0.24.0
spacy>=3.0.0
nltk>=3.6.0
regex>=2021.4.4
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- Your Name - _Initial work_ - [YourGitHub](https://github.com/yourusername)

## Acknowledgments

- SpaCy for NLP capabilities
- PyPDF2 for PDF processing
- scikit-learn for text analysis
- All other open-source libraries used in this project
