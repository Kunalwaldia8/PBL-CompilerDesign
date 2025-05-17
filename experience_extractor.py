import re
import spacy

# Simple function to locate the experience section
def extract_experience_section(text):
    experience_keywords = [
        "experience", "work experience", "professional experience",
        "internship", "employment history"
    ]
    text_lower = text.lower()
    for keyword in experience_keywords:
        if keyword in text_lower:
            idx = text_lower.index(keyword)
            return text[idx:]
    return ""  # if nothing found

# Extract date ranges like: Jan 2021 – Feb 2023
def extract_date_ranges(text):
    date_pattern = r"(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*[.,]?\s?\d{4}\s?[-–to]+\s?(present|\d{4})"
    return re.findall(date_pattern, text, flags=re.IGNORECASE)

# Extract bullet-style or sentence-based descriptions
def extract_experience_descriptions(section_text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(section_text)
    experience_sentences = []
    for sent in doc.sents:
        if len(sent.text.strip()) > 20:  # avoid very short lines
            experience_sentences.append(sent.text.strip())
    return experience_sentences

# Final function to call from your pipeline
def extract_experience(text):
    section = extract_experience_section(text)
    if not section:
        return {"raw_text": "", "highlights": []}
    
    highlights = extract_experience_descriptions(section)
    return {
        "raw_text": section.strip(),
        "highlights": highlights
    }
