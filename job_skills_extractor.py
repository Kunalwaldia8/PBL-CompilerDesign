# job_skills_extractor.py

import re
import spacy
import pandas as pd
from collections import Counter

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Common skill keywords and patterns
COMMON_TECH_SKILLS = [
    "python", "java", "javascript", "html", "css", "sql", "nosql", "aws", 
    "azure", "gcp", "docker", "kubernetes", "react", "angular", "vue", 
    "node.js", "express", "django", "flask", "spring", "hibernate", 
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "r", 
    "tableau", "power bi", "excel", "word", "powerpoint", "git", "github",
    "gitlab", "ci/cd", "jenkins", "agile", "scrum", "kanban", "jira"
]

# Function to extract skills from job description
def extract_skills_from_job(job_description):
    """
    Extract skills from a job description using NLP techniques.
    
    Args:
        job_description (str): The job description text
        
    Returns:
        list: List of extracted skills
    """
    # Convert to lowercase for better matching
    text = job_description.lower()
    
    # Process with spaCy
    doc = nlp(text)
    
    extracted_skills = []
    
    # Extract skills using noun chunks and named entities
    for chunk in doc.noun_chunks:
        if any(skill in chunk.text.lower() for skill in COMMON_TECH_SKILLS):
            extracted_skills.append(chunk.text.strip())
    
    # Extract skills using regex patterns
    skill_pattern = r'\b(?:proficient in|experience with|knowledge of|skilled in|expertise in)\s+([^.,:;]+)'
    matches = re.findall(skill_pattern, text)
    for match in matches:
        extracted_skills.append(match.strip())
    
    # Direct matching of common skills
    for skill in COMMON_TECH_SKILLS:
        if skill in text:
            extracted_skills.append(skill)
    
    # Clean and normalize skills
    cleaned_skills = []
    for skill in extracted_skills:
        # Remove extra whitespace and common words
        skill = re.sub(r'\s+', ' ', skill).strip()
        skill = re.sub(r'^(and|or|the|a|an|in|with|using)\s+', '', skill)
        if len(skill) > 2:  # Ignore very short skills
            cleaned_skills.append(skill)
    
    # Count occurrences and get unique skills
    skill_counter = Counter(cleaned_skills)
    unique_skills = list(skill_counter.keys())
    
    return unique_skills

# Function to process multiple job descriptions
def process_job_descriptions(job_data):
    """
    Process multiple job descriptions and extract skills.
    
    Args:
        job_data (pd.DataFrame): DataFrame with job descriptions
        
    Returns:
        pd.DataFrame: DataFrame with job IDs and extracted skills
    """
    results = []
    
    for _, row in job_data.iterrows():
        job_id = row.get('Job_ID', None)
        job_desc = row.get('Job_Desc', '')
        
        if not job_desc:
            continue
            
        skills = extract_skills_from_job(job_desc)
        
        results.append({
            'Job_ID': job_id,
            'Skills': ','.join(skills)
        })
    
    return pd.DataFrame(results)

# Example usage
if __name__ == "__main__":
    # Sample job data
    sample_data = pd.DataFrame({
        'Job_ID': [1, 2],
        'Job_Desc': [
            "Applicant should possess technical capabilities including proficient knowledge of python and SQL",
            "Applicant should possess technical capabilities including proficient knowledge of python and SQL and R"
        ]
    })
    
    # Process job descriptions
    result_df = process_job_descriptions(sample_data)
    print(result_df)
    
    # Save to CSV
    result_df.to_csv("extracted_job_skills.csv", index=False)
    print("✅ Job skills data saved to extracted_job_skills.csv")
