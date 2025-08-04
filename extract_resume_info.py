import docx2txt
import PyPDF2
import os

def extract_info(file):
    ext = os.path.splitext(file.name)[1].lower()
    text = ""
    
    if ext == ".pdf":
        reader = PyPDF2.PdfReader(file)
        text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    elif ext == ".docx":
        text = docx2txt.process(file)
    elif ext == ".txt":
        text = file.read().decode("utf-8")

    # Simple heuristics
    skills = []
    with open("skills.txt", "r") as f:
        keywords = [line.strip().lower() for line in f]
        for word in keywords:
            if word in text.lower():
                skills.append(word)

    experience = text[text.lower().find("experience"):]
    return text, skills, experience
