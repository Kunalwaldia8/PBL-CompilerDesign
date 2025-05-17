import re

SECTION_HEADERS = [
    "personal information", "summary", "objective", "profile",
    "work experience", "professional experience", "experience",
    "education", "academic background",
    "skills", "technical skills",
    "projects", "internships",
    "certifications", "licenses",
    "awards", "achievements",
    "publications", "languages"
]

def segment_sections(text):
    sections = {}
    current_section = "unknown"
    buffer = []

    lines = text.split('\n')
    for line in lines:
        line_clean = line.strip().lower()

        # Check for section header
        for header in SECTION_HEADERS:
            pattern = r'\b' + re.escape(header) + r'\b'
            if re.match(pattern, line_clean):
                if buffer:
                    sections[current_section] = '\n'.join(buffer).strip()
                    buffer = []
                current_section = header
                break
        else:
            buffer.append(line)

    # Add remaining buffer
    if buffer:
        sections[current_section] = '\n'.join(buffer).strip()

    return sections
