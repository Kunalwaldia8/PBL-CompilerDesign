# skill_matcher_main.py

import pandas as pd
from job_skills_extractor import process_job_descriptions, extract_skills_from_job
from resume_job_matcher import rank_candidates

def extract_resume_skills(resume_data):
    """
    Extract skills from resume data.
    
    Args:
        resume_data (pd.DataFrame): DataFrame with resume data
        
    Returns:
        pd.DataFrame: DataFrame with candidate IDs and extracted skills
    """
    results = []
    
    for _, row in resume_data.iterrows():
        candidate_id = row.get('Candidate_ID', None)
        resume_text = row.get('Resume_Text', '')
        
        if not resume_text:
            continue
            
        # Reuse the same extraction function for consistency
        skills = extract_skills_from_job(resume_text)
        
        results.append({
            'Candidate_ID': candidate_id,
            'Skills': ','.join(skills)
        })
    
    return pd.DataFrame(results)

def main():
    """
    Main function to process job descriptions and resumes, and rank candidates.
    """
    # Load job data
    job_data = pd.read_csv("job_descriptions.csv")
    
    # Extract skills from job descriptions
    job_skills_df = process_job_descriptions(job_data)
    job_skills_df.to_csv("extracted_job_skills.csv", index=False)
    print("✅ Job skills data saved to extracted_job_skills.csv")
    
    # Load resume data
    resume_data = pd.read_csv("resume_data.csv")
    
    # Extract skills from resumes
    resume_skills_df = extract_resume_skills(resume_data)
    resume_skills_df.to_csv("extracted_resume_skills.csv", index=False)
    print("✅ Resume skills data saved to extracted_resume_skills.csv")
    
    # Rank candidates
    rankings_df = rank_candidates(resume_skills_df, job_skills_df)
    rankings_df.to_csv("candidate_rankings.csv", index=False)
    print("✅ Candidate rankings saved to candidate_rankings.csv")
    
    # Display top candidates for each job
    for job_id in job_skills_df['Job_ID'].unique():
        print(f"\nTop 3 candidates for Job ID {job_id}:")
        top_candidates = rankings_df[rankings_df['Job_ID'] == job_id].sort_values('Rank').head(3)
        for _, candidate in top_candidates.iterrows():
            print(f"  Rank {candidate['Rank']}: Candidate {candidate['Candidate_ID']} - Match Score: {candidate['Match_Score']:.2f}, Final Score: {candidate['Final_Score']:.2f}")
            print(f"    Matching Skills: {candidate['Matching_Skills']}")
            print(f"    Missing Skills: {candidate['Missing_Skills']}")

if __name__ == "__main__":
    main()
