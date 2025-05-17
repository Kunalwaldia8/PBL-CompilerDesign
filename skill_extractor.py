import re
import spacy
from pathlib import Path

class SkillExtractor:
    def __init__(self, skills_file="skills.txt"):
        """Initialize the skill extractor with a skills dictionary."""
        self.nlp = spacy.load("en_core_web_sm")
        self.skills = self._load_skills(skills_file)
        self.skill_patterns = self._compile_skill_patterns()

    def _load_skills(self, skills_file):
        """Load skills from the skills dictionary file."""
        skills_path = Path(skills_file)
        if not skills_path.exists():
            raise FileNotFoundError(f"Skills file not found: {skills_file}")
            
        with open(skills_path, 'r') as f:
            return [line.strip().lower() for line in f if line.strip()]

    def _compile_skill_patterns(self):
        """Compile regex patterns for skill matching."""
        patterns = []
        for skill in self.skills:
            # Handle special characters in skill names
            escaped_skill = re.escape(skill)
            # Match whole words only, case insensitive
            pattern = re.compile(r'\b' + escaped_skill + r'\b', re.IGNORECASE)
            patterns.append((skill, pattern))
        return patterns

    def extract_skills(self, text):
        """
        Extract skills from the given text.
        
        Args:
            text (str): Input text to extract skills from
            
        Returns:
            list: List of unique skills found in the text
        """
        found_skills = set()
        
        # Convert text to lowercase for better matching
        text_lower = text.lower()
        
        # Use regex patterns to find skills
        for skill, pattern in self.skill_patterns:
            if pattern.search(text_lower):
                found_skills.add(skill)
        
        # Use spaCy for additional entity recognition
        doc = self.nlp(text)
        
        # Extract potential skills from noun phrases
        for chunk in doc.noun_chunks:
            skill_candidate = chunk.text.lower()
            # Check if the noun phrase matches any skill in our dictionary
            for skill in self.skills:
                if skill == skill_candidate:
                    found_skills.add(skill)
        
        return sorted(list(found_skills))

    def extract_skills_with_context(self, text, context_words=10):
        """
        Extract skills with surrounding context.
        
        Args:
            text (str): Input text to extract skills from
            context_words (int): Number of words to include as context before and after
            
        Returns:
            list: List of tuples containing (skill, context)
        """
        skills_context = []
        words = text.split()
        
        for i, _ in enumerate(words):
            # Get the context window
            start = max(0, i - context_words)
            end = min(len(words), i + context_words + 1)
            context = ' '.join(words[start:end])
            
            # Check each skill pattern in this context
            for skill, pattern in self.skill_patterns:
                if pattern.search(context):
                    skills_context.append({
                        'skill': skill,
                        'context': context.strip()
                    })
        
        return skills_context

def main():
    """
    Example usage of the SkillExtractor class.
    """
    # Initialize the extractor
    extractor = SkillExtractor()
    
    # Example text
    sample_text = """
    Experienced software developer with expertise in Python and JavaScript.
    Proficient in React.js and Node.js development.
    Strong background in data structures and algorithms.
    Experience with Git version control and agile development methodologies.
    """
    
    # Extract skills
    skills = extractor.extract_skills(sample_text)
    print("Found skills:", skills)
    
    # Extract skills with context
    skills_context = extractor.extract_skills_with_context(sample_text)
    print("\nSkills with context:")
    for item in skills_context:
        print(f"\nSkill: {item['skill']}")
        print(f"Context: {item['context']}")

if __name__ == "__main__":
    main()
