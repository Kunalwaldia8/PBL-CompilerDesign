import re
import json
from pathlib import Path

class SectionSegmenter:
    def __init__(self, patterns_file="data/section_patterns.json"):
        """
        Initialize the section segmenter with section patterns.
        
        Args:
            patterns_file (str): Path to JSON file containing section patterns
        """
        self.section_patterns = self._load_patterns(patterns_file)
        self._compile_patterns()

    def _load_patterns(self, patterns_file):
        """Load section patterns from JSON file."""
        default_patterns = {
            "education": [
                "education",
                "academic background",
                "academic qualification",
                "educational qualification",
                "academic history"
            ],
            "experience": [
                "experience",
                "work experience",
                "employment history",
                "work history",
                "professional experience",
                "professional background"
            ],
            "skills": [
                "skills",
                "technical skills",
                "core competencies",
                "key skills",
                "technical expertise",
                "technologies"
            ],
            "projects": [
                "projects",
                "project experience",
                "academic projects",
                "personal projects",
                "key projects"
            ],
            "summary": [
                "summary",
                "professional summary",
                "profile summary",
                "career objective",
                "objective"
            ],
            "achievements": [
                "achievements",
                "honors",
                "awards",
                "accomplishments",
                "certifications"
            ]
        }

        try:
            if Path(patterns_file).exists():
                with open(patterns_file, 'r') as f:
                    return json.load(f)
            return default_patterns
        except Exception as e:
            print(f"Warning: Could not load patterns file: {e}")
            return default_patterns

    def _compile_patterns(self):
        """Compile regex patterns for section matching."""
        self.compiled_patterns = {}
        for section, patterns in self.section_patterns.items():
            # Create pattern that matches any of the section headers
            pattern = '|'.join(f'(?:{p})' for p in patterns)
            # Case insensitive, matches start of line or after newline
            self.compiled_patterns[section] = re.compile(
                f'^(?:{pattern}):?\\s*$',
                re.IGNORECASE | re.MULTILINE
            )

    def identify_section_bounds(self, text):
        """
        Identify the boundaries of each section in the text.
        
        Args:
            text (str): Resume text to segment
            
        Returns:
            dict: Dictionary with section names and their start/end positions
        """
        # Find all section matches
        sections = {}
        for section, pattern in self.compiled_patterns.items():
            for match in pattern.finditer(text):
                sections[match.start()] = {
                    'name': section,
                    'start': match.start(),
                    'header': match.group()
                }

        # Sort sections by their starting position
        sorted_positions = sorted(sections.keys())

        # Determine section boundaries
        section_bounds = {}
        for i, pos in enumerate(sorted_positions):
            section = sections[pos]
            section_name = section['name']
            start = pos
            
            # End is either the start of next section or end of text
            if i < len(sorted_positions) - 1:
                end = sorted_positions[i + 1]
            else:
                end = len(text)

            section_bounds[section_name] = {
                'start': start,
                'end': end,
                'header': section['header']
            }

        return section_bounds

    def extract_sections(self, text):
        """
        Extract sections from resume text.
        
        Args:
            text (str): Resume text to segment
            
        Returns:
            dict: Dictionary with section names and their content
        """
        # Get section boundaries
        bounds = self.identify_section_bounds(text)
        
        # Extract content for each section
        sections = {}
        for section, pos in bounds.items():
            content = text[pos['start']:pos['end']].strip()
            # Remove the header from the content
            content = re.sub(f"^{re.escape(pos['header'])}", '', content, flags=re.MULTILINE)
            sections[section] = content.strip()
        
        return sections

    def get_section(self, text, section_name):
        """
        Extract a specific section from the text.
        
        Args:
            text (str): Resume text
            section_name (str): Name of the section to extract
            
        Returns:
            str: Content of the requested section, or None if not found
        """
        sections = self.extract_sections(text)
        return sections.get(section_name)

def main():
    """Example usage of the SectionSegmenter."""
    # Sample resume text
    sample_text = """
EDUCATION:
B.S. in Computer Science
University of Example, 2018-2022
GPA: 3.8/4.0

EXPERIENCE:
Software Engineer Intern
Tech Company Inc., Summer 2021
- Developed features for web application
- Collaborated with team members

SKILLS:
Programming Languages: Python, Java, JavaScript
Frameworks: React, Node.js
Tools: Git, Docker

PROJECTS:
Personal Website
- Built using React and Node.js
- Deployed on AWS
    """
    
    # Initialize segmenter
    segmenter = SectionSegmenter()
    
    # Extract all sections
    sections = segmenter.extract_sections(sample_text)
    
    # Print each section
    for section_name, content in sections.items():
        print(f"\n{section_name.upper()}:")
        print(content)
        print("-" * 50)

if __name__ == "__main__":
    main()
