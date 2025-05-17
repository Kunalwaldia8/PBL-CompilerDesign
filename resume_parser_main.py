import json
from entity_extractor import (
    extract_name, extract_email, extract_phone,
    extract_skills, extract_github_url, extract_linkedin_url,
    extract_education, extract_projects
)

from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    text = ''
    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

if __name__ == "__main__":
    path = r"data/kunalResume.pdf"  # Replace with your resume file path
    resume_text = extract_text_from_pdf(path)

    extracted_data = {
    "name": extract_name(resume_text),
    "email": extract_email(resume_text),
    "phone": extract_phone(resume_text),
    "skills": extract_skills(resume_text),
    "github": extract_github_url(resume_text),
    "linkedin": extract_linkedin_url(resume_text),
    "education": extract_education(resume_text)
}


    with open("output.txt", "w") as f:
        json.dump(extracted_data, f, indent=4)

    print("✅ Resume data saved to output.txt")
