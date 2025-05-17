from input_handler import extract_text_from_pdf
from skill_extractor import extract_all_skills

# Load skills from file
with open("skills.txt", "r") as f:
    skills_list = [line.strip() for line in f if line.strip()]
text = extract_text_from_pdf("kunalResume.pdf")
skills = extract_all_skills(text, skills_list)

print("Extracted Skills:")
for skill in skills:
    print("✅", skill)
