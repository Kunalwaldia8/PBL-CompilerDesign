import spacy
import re
import json

nlp = spacy.load("en_core_web_sm")
# English language model

def extract_email(text):
    match = re.findall(r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+", text)
    return match[0] if match else None

def extract_phone(text):
    match = re.findall(r"\+?\d[\d -]{8,12}\d", text)
    return match[0] if match else None

def extract_skills(text):
    predefined_skills = ["Python", "Java", "Machine Learning", "SQL", "React", "Node.js"]
    skills_found = [skill for skill in predefined_skills if skill.lower() in text.lower()]
    return skills_found

def extract_resume_info(text):
    doc = nlp(text)
    name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break
    return {
        "Name": name,
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "Skills": extract_skills(text)
    }

# Example Usage
# resume_text = "John Doe\nEmail: johndoe@email.com\nPhone: +123456789\nSkills: Python, Java, SQL"

f=open("output.txt","r")
file_data=f.read()
parsed_data = extract_resume_info(file_data)
print(parsed_data)


# Convert Extracted Data to JSON :

def convert_to_json(parsed_data):
    return json.dumps(parsed_data, indent=4)

# Example Usage
json_output = convert_to_json(parsed_data)
print("\n\n"+json_output)

f = open("json_output.txt", "w")
f.write(json_output)
f.close()