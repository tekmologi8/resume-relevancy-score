from fpdf import FPDF
import os

def generate_pdf_report(filename, score, skills, experience):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Resume Relevancy Report", ln=1, align='C')
    pdf.cell(200, 10, txt=f"Filename: {filename}", ln=2, align='L')
    pdf.cell(200, 10, txt=f"Score: {score:.2f}%", ln=3, align='L')

    pdf.multi_cell(0, 10, txt=f"\nSkills: {', '.join(skills)}")
    pdf.multi_cell(0, 10, txt=f"\nExperience (snippet):\n{experience[:800]}")

    path = os.path.join("reports", filename.replace(" ", "_") + "_report.pdf")
    pdf.output(path)
    return path
