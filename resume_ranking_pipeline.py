import json
import os
import re
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Import from your existing entity extractor
from entity_extractor import (
    extract_name, extract_email, extract_phone,
    extract_skills, extract_github_url, extract_linkedin_url,
    extract_education, extract_projects
)

from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    """Extract text content from a PDF file."""
    text = ''
    try:
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
    return text

def extract_skills_from_job_description(job_description_text):
    """Extract skills from job description using similar methods as resume skills extraction."""
    # This should use the same skill extraction logic as in entity_extractor.py
    # For demonstration, I'll use a simple implementation
    # In production, this should match your extract_skills function
    
     # Read skills from skill.txt file
    try:
        with open("skills.txt", "r") as skill_file:
            common_skills = [line.strip().lower() for line in skill_file if line.strip()]
    except FileNotFoundError:
        print("Warning: skill.txt file not found. Using a minimal default skill list.")
        # Fallback to a minimal list if file not found
        common_skills = ["python", "java", "javascript", "sql"]
    
    # Extract skills using regex pattern matching
    skills = []
    for skill in common_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', job_description_text.lower()):
            skills.append(skill)
    
    # You can enhance this with more sophisticated extraction methods
    return skills

def calculate_skill_match_score(resume_skills, job_skills):
    """Calculate a match score between resume skills and job description skills."""
    if not resume_skills or not job_skills:
        return 0.0
    
    # Convert skills to lowercase for better matching
    resume_skills_lower = [skill.lower() for skill in resume_skills]
    job_skills_lower = [skill.lower() for skill in job_skills]
    
    # Count matching skills
    matching_skills = set(resume_skills_lower).intersection(set(job_skills_lower))
    
    # Calculate match percentage based on job requirements
    match_score = len(matching_skills) / len(job_skills_lower) if job_skills_lower else 0
    
    return match_score * 100  # Return as percentage

def calculate_semantic_similarity(resume_text, job_description_text):
    """Calculate semantic similarity between resume and job description using cosine similarity."""
    if not resume_text or not job_description_text:
        return 0.0
    
    # Create a vectorizer
    vectorizer = CountVectorizer(stop_words='english')
    
    try:
        # Create the document-term matrix
        count_matrix = vectorizer.fit_transform([resume_text, job_description_text])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(count_matrix)[0][1]
        return similarity * 100  # Return as percentage
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0

def process_resume(file_path):
    """Process a single resume and extract relevant information."""
    resume_text = extract_text_from_pdf(file_path)
    
    # Extract data using your existing functions
    extracted_data = {
        "name": extract_name(resume_text),
        "email": extract_email(resume_text),
        "phone": extract_phone(resume_text),
        "skills": extract_skills(resume_text),
        "github": extract_github_url(resume_text),
        "linkedin": extract_linkedin_url(resume_text),
        "education": extract_education(resume_text),
        "full_text": resume_text  # Store full text for semantic similarity
    }
    
    return extracted_data

def rank_resumes(resumes_data, job_description_text):
    """Rank resumes based on their match with the job description."""
    # Extract skills from job description
    job_skills = extract_skills_from_job_description(job_description_text)
    
    # Calculate scores for each resume
    ranked_resumes = []
    for resume_path, resume_data in resumes_data.items():
        # Calculate skill match score (50% weight)
        skill_match = calculate_skill_match_score(resume_data["skills"], job_skills)
        
        # Calculate semantic similarity score (50% weight)
        semantic_score = calculate_semantic_similarity(resume_data["full_text"], job_description_text)
        
        # Calculate final score (weighted average)
        final_score = (skill_match * 0.5) + (semantic_score * 0.5)
        
        # Get resume file name without path
        resume_name = os.path.basename(resume_path)
        
        ranked_resumes.append({
            "resume_name": resume_name,
            "candidate_name": resume_data["name"],
            "skills": resume_data["skills"],
            "matching_skills": list(set([skill.lower() for skill in resume_data["skills"]]).intersection(
                               set([skill.lower() for skill in job_skills]))),
            "missing_skills": list(set([skill.lower() for skill in job_skills]) - 
                               set([skill.lower() for skill in resume_data["skills"]])),
            "skill_match_score": skill_match,
            "semantic_score": semantic_score,
            "final_score": final_score,
            "resume_path": resume_path,
            "contact": {
                "email": resume_data["email"],
                "phone": resume_data["phone"],
                "github": resume_data["github"],
                "linkedin": resume_data["linkedin"]
            },
            "education": resume_data["education"]
        })
    
    # Sort resumes by final score (descending)
    ranked_resumes.sort(key=lambda x: x["final_score"], reverse=True)
    
    # Add rank
    for i, resume in enumerate(ranked_resumes):
        resume["rank"] = i + 1
    
    return ranked_resumes
def generate_html_report(ranked_resumes):
    """Generate an HTML report for the ranked resumes."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Resume Ranking Results</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .container { max-width: 1200px; margin: 0 auto; }
            h1 { color: #2c3e50; }
            .resume-card { 
                border: 1px solid #ddd; 
                border-radius: 8px; 
                padding: 15px; 
                margin-bottom: 20px;
                background-color: #f9f9f9;
            }
            .top-resume { background-color: #e8f5e9; }
            .score { 
                font-size: 24px; 
                font-weight: bold; 
                color: #1976d2;
            }
            .skills-list { 
                display: flex; 
                flex-wrap: wrap; 
                gap: 8px;
            }
            .skill {
                background-color: #e3f2fd;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 14px;
            }
            .missing-skill {
                background-color: #ffebee;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 14px;
            }
            .contact-info {
                display: flex;
                gap: 15px;
                margin-top: 10px;
                font-size: 14px;
            }
            .rank-badge {
                display: inline-block;
                width: 30px;
                height: 30px;
                background-color: #1976d2;
                color: white;
                border-radius: 50%;
                text-align: center;
                line-height: 30px;
                margin-right: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Resume Ranking Results</h1>
            
    """
    
    # Add each resume card
    for resume in ranked_resumes:
        top_class = " top-resume" if resume["rank"] <= 3 else ""
        
        html += f"""
            <div class="resume-card{top_class}">
                <h2><span class="rank-badge">{resume["rank"]}</span>{resume["candidate_name"]}</h2>
                <p>Resume: <strong>{resume["resume_name"]}</strong></p>
                <p>Score: <span class="score">{resume["final_score"]:.2f}%</span></p>
                <p>Skill Match: {resume["skill_match_score"]:.2f}% | Semantic Match: {resume["semantic_score"]:.2f}%</p>
                
                <h3>Matching Skills:</h3>
                <div class="skills-list">
        """
        
        # Add matching skills
        for skill in resume["matching_skills"]:
            html += f'<span class="skill">{skill}</span>'
        
        html += """
                </div>
                
                <h3>Missing Skills:</h3>
                <div class="skills-list">
        """
        
        # Add missing skills
        for skill in resume["missing_skills"]:
            html += f'<span class="missing-skill">{skill}</span>'
        
        html += """
                </div>
                
                <h3>Contact Information:</h3>
                <div class="contact-info">
        """
        
        # Add contact info
        if resume["contact"]["email"]:
            html += f'<span>📧 {resume["contact"]["email"]}</span>'
        if resume["contact"]["phone"]:
            html += f'<span>📱 {resume["contact"]["phone"]}</span>'
        if resume["contact"]["github"]:
            html += f'<span>GitHub: {resume["contact"]["github"]}</span>'
        if resume["contact"]["linkedin"]:
            html += f'<span>LinkedIn: {resume["contact"]["linkedin"]}</span>'
        
        html += """
                </div>
            </div>
        """
    
    html += """
        </div>
    </body>
    </html>
    """
    
    # Save HTML report
    with open("resume_ranking_report.html", "w") as f:
        f.write(html)
    
    print(f"✅ HTML report saved to resume_ranking_report.html")

def main():
    # Path to job description file
    job_description_path = "data/job_description.txt"
    
    # Path to directory containing resumes
    resumes_dir = "data/resumes"
    
    # Read job description
    try:
        with open(job_description_path, 'r') as f:
            job_description_text = f.read()
    except FileNotFoundError:
        print(f"Job description file not found at {job_description_path}")
        return
    
    # Process all resumes in the directory
    resumes_data = {}
    resume_files = [f for f in os.listdir(resumes_dir) if f.endswith('.pdf')]
    
    if not resume_files:
        print(f"No PDF resumes found in {resumes_dir}")
        return
    
    print(f"Processing {len(resume_files)} resumes...")
    
    for resume_file in resume_files:
        resume_path = os.path.join(resumes_dir, resume_file)
        print(f"Processing {resume_file}...")
        resumes_data[resume_path] = process_resume(resume_path)
    
    # Rank resumes
    ranked_resumes = rank_resumes(resumes_data, job_description_text)
    
    # Save results to JSON
    output_path = "ranked_resumes.json"
    with open(output_path, "w") as f:
        json.dump(ranked_resumes, f, indent=4)
    
    print(f"✅ Ranked resumes saved to {output_path}")
    # Generate HTML report
    generate_html_report(ranked_resumes) 
    # Display top candidates
    print("\nTop Candidates:")
    for resume in ranked_resumes[:3]:  # Display top 3
        print(f"{resume['rank']}. {resume['candidate_name']} - Score: {resume['final_score']:.2f}%")
        print(f"   Resume: {resume['resume_name']}")
        print(f"   Matching Skills: {', '.join(resume['matching_skills'])}")
        print(f"   Missing Skills: {', '.join(resume['missing_skills'])}")
        print()
    
    # Create a summary DataFrame for easy viewing
    summary_df = pd.DataFrame([
        {
            "Rank": r["rank"],
            "Name": r["candidate_name"],
            "Resume": r["resume_name"],
            "Score": f"{r['final_score']:.2f}%",
            "Skill Match": f"{r['skill_match_score']:.2f}%",
            "Semantic Match": f"{r['semantic_score']:.2f}%",
            "Matching Skills Count": len(r["matching_skills"]),
            "Missing Skills Count": len(r["missing_skills"])
        }
        for r in ranked_resumes
    ])
    
    # Save summary to CSV
    summary_df.to_csv("resume_ranking_summary.csv", index=False)
    print(f"✅ Summary saved to resume_ranking_summary.csv")

if __name__ == "__main__":
    main()
