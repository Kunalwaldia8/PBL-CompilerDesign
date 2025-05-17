import re
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# ------------ NAME EXTRACTION ----------------
def extract_name(text):
    lines = text.strip().split("\n")[:5]
    for line in lines:
        match = re.match(r"(?i)^name[:\-]?\s*([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)", line)
        if match:
            return match.group(1)

    match = re.search(r"\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b", text)
    if match:
        return f"{match.group(1)} {match.group(2)}"

    match = re.search(r"\b([A-Z]{2,})\s+([A-Z]{2,})\b", text)
    if match:
        return f"{match.group(1).title()} {match.group(2).title()}"
    
    return None

# ------------ EMAIL EXTRACTION ----------------
def extract_email(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[\s]*[a-zA-Z0-9.-]+[\s]*\.[a-zA-Z]{2,}"
    matches = re.findall(pattern, text)
    if matches:
        return matches[0].replace(" ", "").strip()
    return None

# ------------ PHONE EXTRACTION ----------------
def extract_phone(text):
    pattern = r"(?:\+91[\-\s]?)?[6-9]\d{9}"
    matches = re.findall(pattern, text)
    return matches[0] if matches else None

# ------------ SKILL EXTRACTION ----------------
def extract_skills(text):
    skills_keywords = [
        'c++', 'java', 'python', 'html', 'css', 'javascript', 'sql',
        'react', 'reactjs', 'nodejs', 'expressjs', 'mongodb', 'git',
        'github', 'bootstrap', 'tailwind css',
        'object-oriented programming', 'data structures', 'algorithms'
    ]

    text = text.lower()
    found_skills = set()
    for skill in skills_keywords:
        if skill.lower() in text:
            found_skills.add(skill)

    return list(found_skills)

# ------------ GITHUB EXTRACTION ----------------
def extract_github_url(text):
    pattern = r"(https?://)?(www\.)?github\.com/[a-zA-Z0-9_-]+"
    match = re.search(pattern, text.replace(" ", ""))
    return match.group(0) if match else None

# ------------ LINKEDIN EXTRACTION ----------------
def extract_linkedin_url(text):
    pattern = r"(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+"
    match = re.search(pattern, text.replace(" ", ""))
    return match.group(0) if match else None

# ------------ EDUCATION EXTRACTION ----------------
def extract_education(text):
    # Common course name keywords
    course_keywords = [
        "b\.?tech", "bachelor of technology", "b\.?e", "bachelor of engineering",
        "bsc", "b\.?sc", "bachelor of science",
        "bca", "b\.?c\.?a",
        "m\.?tech", "master of technology", "m\.?e", "master of engineering",
        "msc", "m\.?sc", "master of science",
        "mca", "m\.?c\.?a",
        "ph\.?d", "high school", "secondary school", "senior secondary"
    ]

    text = text.lower()
    found_courses = set()

    for keyword in course_keywords:
        matches = re.findall(rf"\b{keyword}\b", text)
        for match in matches:
            clean = match.replace(".", "").strip()
            found_courses.add(clean.upper())

    return list(found_courses) if found_courses else None


# ------------ PROJECTS EXTRACTION ----------------
def extract_projects(text):
    project_keywords = ["project", "clone", "system", "detection", "app", "application", "implementation"]
    lines = text.lower().split("\n")
    projects = []

    for i, line in enumerate(lines):
        if any(k in line for k in project_keywords):
            project_block = line
            # Optionally append next few lines to capture description
            for j in range(1, 3):
                if i + j < len(lines):
                    project_block += " " + lines[i + j].strip()
            projects.append(project_block.strip())

    return projects if projects else None
