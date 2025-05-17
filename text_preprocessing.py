import re

def clean_text(text):
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove non-ASCII characters
    text = text.encode('ascii', errors='ignore').decode()
    
    # Remove control characters and extra symbols
    text = re.sub(r'[^\x20-\x7E]', '', text)  # non-printables
    text = re.sub(r'[\u2022\u25CF]', '-', text)  # bullet points to dashes
    text = re.sub(r'[^\w\s\.,:;\-@()&+/]', '', text)  # optional punctuation keep list

    # Fix spacing around punctuation
    text = re.sub(r'\s+([.,:;!?()])', r'\1', text)
    text = re.sub(r'([.,:;!?()])([^\s])', r'\1 \2', text)

    return text.strip()
