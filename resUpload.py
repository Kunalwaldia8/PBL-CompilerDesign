import pdfplumber
import docx

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open("sample_pdf/divyansh_resume_2025_new_1.pdf") as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(docx_path):
    doc = docx.Document("sample_pdf/divyansh_resume_2025_new_1.docx")
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Example usage
pdf_text = extract_text_from_pdf("resume.pdf")
docx_text = extract_text_from_docx("resume.docx")
print(pdf_text)  # View extracted text
# print(docx_text)  # View extracted text

f = open("output.txt", "w")
f.write(pdf_text)
f.close()