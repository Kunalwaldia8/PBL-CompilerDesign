# resume_job_matcher.py

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_data(resume_skills_path, job_skills_path):
    """
    Load resume skills and job skills data.
    
    Args:
        resume_skills_path (str): Path to resume skills CSV
        job_skills_path (str): Path to job skills CSV
        
    Returns:
        tuple: (resume_df, job_df)
    """
    resume_df = pd.read_csv(resume_skills_path)
    job_df = pd.read_csv(job_skills_path)
    return resume_df, job_df

def calculate_skill_match(resume_skills, job_skills):
    """
    Calculate skill match score between resume and job.
    
    Args:
        resume_skills (str): Comma-separated skills from resume
        job_skills (str): Comma-separated skills from job
        
    Returns:
        float: Match score (0-1)
    """
    if not resume_skills or not job_skills:
        return 0.0
    
    # Convert comma-separated strings to lists
    resume_skill_list = [skill.strip().lower() for skill in resume_skills.split(',')]
    job_skill_list = [skill.strip().lower() for skill in job_skills.split(',')]
    
    # Count matching skills
    matching_skills = set(resume_skill_list).intersection(set(job_skill_list))
    
    # Calculate match percentage based on job requirements
    match_score = len(matching_skills) / len(job_skill_list) if job_skill_list else 0
    
    return match_score

def calculate_similarity_score(resume_skills, job_skills):
    """
    Calculate similarity score using cosine similarity.
    
    Args:
        resume_skills (str): Comma-separated skills from resume
        job_skills (str): Comma-separated skills from job
        
    Returns:
        float: Similarity score (0-1)
    """
    if not resume_skills or not job_skills:
        return 0.0
    
    # Create a vectorizer
    vectorizer = CountVectorizer()
    
    # Combine skills into documents
    documents = [resume_skills, job_skills]
    
    # Create the document-term matrix
    try:
        count_matrix = vectorizer.fit_transform(documents)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(count_matrix)[0][1]
        return similarity
    except:
        return 0.0

def rank_candidates(resume_df, job_df):
    """
    Rank candidates for each job based on skill matching.
    
    Args:
        resume_df (pd.DataFrame): DataFrame with resume skills
        job_df (pd.DataFrame): DataFrame with job skills
        
    Returns:
        pd.DataFrame: DataFrame with rankings
    """
    results = []
    
    for _, job_row in job_df.iterrows():
        job_id = job_row['Job_ID']
        job_skills = job_row['Skills']
        
        job_rankings = []
        
        for _, resume_row in resume_df.iterrows():
            candidate_id = resume_row['Candidate_ID']
            resume_skills = resume_row['Skills']
            
            # Calculate match score
            match_score = calculate_skill_match(resume_skills, job_skills)
            
            # Calculate similarity score
            similarity_score = calculate_similarity_score(resume_skills, job_skills)
            
            # Calculate weighted final score (can adjust weights as needed)
            final_score = 0.7 * match_score + 0.3 * similarity_score
            
            # Get matching skills
            resume_skill_list = [skill.strip().lower() for skill in resume_skills.split(',')]
            job_skill_list = [skill.strip().lower() for skill in job_skills.split(',')]
            matching_skills = set(resume_skill_list).intersection(set(job_skill_list))
            missing_skills = set(job_skill_list) - set(resume_skill_list)
            
            job_rankings.append({
                'Job_ID': job_id,
                'Candidate_ID': candidate_id,
                'Match_Score': match_score,
                'Similarity_Score': similarity_score,
                'Final_Score': final_score,
                'Matching_Skills': ','.join(matching_skills),
                'Missing_Skills': ','.join(missing_skills)
            })
        
        # Sort candidates by final score for this job
        job_rankings.sort(key=lambda x: x['Final_Score'], reverse=True)
        
        # Add rank
        for i, ranking in enumerate(job_rankings):
            ranking['Rank'] = i + 1
            results.append(ranking)
    
    return pd.DataFrame(results)

def main(resume_skills_path, job_skills_path, output_path):
    """
    Main function to rank candidates for jobs.
    
    Args:
        resume_skills_path (str): Path to resume skills CSV
        job_skills_path (str): Path to job skills CSV
        output_path (str): Path to save rankings
    """
    # Load data
    resume_df, job_df = load_data(resume_skills_path, job_skills_path)
    
    # Rank candidates
    rankings_df = rank_candidates(resume_df, job_df)
    
    # Save rankings
    rankings_df.to_csv(output_path, index=False)
    print(f"✅ Candidate rankings saved to {output_path}")

if __name__ == "__main__":
    # Example usage
    resume_skills_path = "extracted_resume_skills.csv"
    job_skills_path = "extracted_job_skills.csv"
    output_path = "candidate_rankings.csv"
    
    main(resume_skills_path, job_skills_path, output_path)
