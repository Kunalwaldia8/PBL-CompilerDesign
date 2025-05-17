import spacy
from spacy.matcher import PhraseMatcher

def load_skills(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        skills = [line.strip().lower() for line in f if line.strip()]
    return list(set(skills))  # Remove duplicates

def build_skill_matcher(nlp, skill_list):
    matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
    patterns = [nlp.make_doc(skill) for skill in skill_list]
    matcher.add("SKILLS", patterns)
    return matcher

def extract_skills(text, skill_list):
    nlp = spacy.load("en_core_web_sm")
    matcher = build_skill_matcher(nlp, skill_list)
    doc = nlp(text.lower())  # Normalize input text
    matches = matcher(doc)
    found_skills = set([doc[start:end].text.strip().lower() for match_id, start, end in matches])
    return sorted(found_skills)
