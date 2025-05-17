import re
import spacy
from datetime import datetime
from section_segmenter import SectionSegmenter

class ExperienceExtractor:
    def __init__(self):
        """Initialize the experience extractor with NLP model."""
        self.nlp = spacy.load("en_core_web_sm")
        self.segmenter = SectionSegmenter()
        
        # Patterns for date extraction
        self.date_patterns = [
            r'((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|'
            r'Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|'
            r'Dec(?:ember)?)[,]?\s+\d{4})',  # Month Year
            r'(\d{1,2}/\d{4})',  # MM/YYYY
            r'(\d{4})',  # YYYY
        ]
        
        # Compile patterns
        self.date_patterns = [re.compile(pattern) for pattern in self.date_patterns]

    def extract_dates(self, text):
        """Extract dates from text using various patterns."""
        dates = []
        for pattern in self.date_patterns:
            matches = pattern.finditer(text)
            for match in matches:
                date_str = match.group(1)
                try:
                    # Try to parse the date
                    if '/' in date_str:
                        date = datetime.strptime(date_str, '%m/%Y')
                    elif len(date_str) == 4:  # Year only
                        date = datetime.strptime(date_str, '%Y')
                    else:  # Month Year
                        date = datetime.strptime(date_str, '%B %Y')
                    dates.append({
                        'date': date,
                        'original': date_str,
                        'position': match.span()
                    })
                except ValueError:
                    continue
        return sorted(dates, key=lambda x: x['position'][0])

    def extract_company_names(self, text):
        """Extract company names using NLP."""
        doc = self.nlp(text)
        companies = []
        
        # Look for organization entities
        for ent in doc.ents:
            if ent.label_ == 'ORG':
                companies.append({
                    'name': ent.text,
                    'position': (ent.start_char, ent.end_char)
                })
        
        return companies

    def extract_job_titles(self, text):
        """Extract job titles from text."""
        common_titles = [
            'software engineer', 'developer', 'architect', 'manager',
            'director', 'consultant', 'analyst', 'specialist', 'lead',
            'administrator', 'coordinator', 'designer', 'intern'
        ]
        
        titles = []
        doc = self.nlp(text.lower())
        
        # Look for job titles at the beginning of lines
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Check if line starts with a common title
            lower_line = line.lower()
            for title in common_titles:
                if lower_line.startswith(title) or title in lower_line:
                    titles.append({
                        'title': line,
                        'confidence': 'high' if lower_line.startswith(title) else 'medium'
                    })
                    break
        
        return titles

    def extract_responsibilities(self, text):
        """Extract job responsibilities and achievements."""
        responsibilities = []
        
        # Split text into lines
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            # Look for bullet points or dashes
            if line.startswith(('-', '•', '∙', '●', '*')) or re.match(r'^\d+\.', line):
                # Clean up the line
                clean_line = line.lstrip('- •∙●*').strip()
                if clean_line:
                    responsibilities.append(clean_line)
        
        return responsibilities

    def analyze_experience(self, text):
        """
        Analyze the complete work experience section.
        
        Args:
            text (str): Full resume text or experience section text
            
        Returns:
            list: List of dictionaries containing structured experience data
        """
        # If full resume text provided, extract experience section
        if len(text.split('\n')) > 10:  # Arbitrary threshold
            text = self.segmenter.get_section(text, 'experience') or text
        
        # Split into different roles (assuming double newline separation)
        roles = re.split(r'\n\s*\n', text)
        experiences = []
        
        for role in roles:
            if not role.strip():
                continue
                
            experience = {}
            
            # Extract dates
            dates = self.extract_dates(role)
            if dates:
                experience['start_date'] = dates[0]['original']
                if len(dates) > 1:
                    experience['end_date'] = dates[-1]['original']
                else:
                    experience['end_date'] = 'Present'
            
            # Extract company names
            companies = self.extract_company_names(role)
            if companies:
                experience['company'] = companies[0]['name']
            
            # Extract job titles
            titles = self.extract_job_titles(role)
            if titles:
                experience['title'] = titles[0]['title']
            
            # Extract responsibilities
            experience['responsibilities'] = self.extract_responsibilities(role)
            
            if any(experience.values()):  # Only add if we found some information
                experiences.append(experience)
        
        return experiences

def main():
    """Example usage of ExperienceExtractor."""
    # Sample text
    sample_text = """
EXPERIENCE

Senior Software Engineer
TechCorp Industries
January 2020 - Present
• Led development of microservices architecture
• Mentored junior developers
• Implemented CI/CD pipeline

Software Developer
StartupCo
March 2018 - December 2019
• Developed full-stack web applications
• Collaborated with cross-functional teams
• Improved application performance by 40%
    """
    
    extractor = ExperienceExtractor()
    experiences = extractor.analyze_experience(sample_text)
    
    # Print results
    for i, exp in enumerate(experiences, 1):
        print(f"\nExperience {i}:")
        print("=" * 50)
        for key, value in exp.items():
            if isinstance(value, list):
                print(f"\n{key.title()}:")
                for item in value:
                    print(f"- {item}")
            else:
                print(f"{key.title()}: {value}")

if __name__ == "__main__":
    main()
