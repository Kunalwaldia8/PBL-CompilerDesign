from input_handler import extract_text_from_pdf
from text_processor import clean_text
from skill_extractor import load_skills, extract_skills
from experience_extractor import extract_experience

if __name__ == "__main__":
    pdf_path = "kunalResume.pdf"
    skill_file = "skills.txt"

    raw_text = extract_text_from_pdf(pdf_path)
    print("📄 Raw Text Extracted:")
    print(raw_text[:])  # Print first 500 characters for brevity
    clean = clean_text(raw_text)
    print("\n🧼 Cleaned Text:")
    print(clean[:])  # Print first 500 characters for brevity

    experience = extract_experience(clean)
    print("🎯 Experience Section Found:")
    print(experience["raw_text"])
    print("\n🔹 Highlights:")
    for h in experience["highlights"]:
            print("-", h)
    skills = load_skills(skill_file)
    extracted = extract_skills(clean, skills)

    print("\n🎯 Extracted Skills:")
    for skill in extracted:
        print("✅", skill)
