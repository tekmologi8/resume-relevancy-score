import streamlit as st
import os
import sqlite3
import datetime
from extract_resume_info import extract_info
from resume_matcher import match_resume_to_job
from report_generator import generate_pdf_report
from email_utils import send_email
import pandas as pd

DB_FILE = "resume_logs.db"
REPORTS_DIR = "reports"

os.makedirs(REPORTS_DIR, exist_ok=True)

def log_to_db(name, score, skills, experience):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (timestamp TEXT, name TEXT, score REAL, skills TEXT, experience TEXT)''')
    c.execute("INSERT INTO logs VALUES (?,?,?,?,?)",
              (datetime.datetime.now().isoformat(), name, score, skills, experience))
    conn.commit()
    conn.close()

def export_logs():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM logs", conn)
    df.to_csv("resume_logs.csv", index=False)
    conn.close()
    return "resume_logs.csv"

st.title("Resume Relevancy Scorer")

job_description = st.text_area("Paste Job Description:")

uploaded_file = st.file_uploader("Upload Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

custom_skills = st.text_area("Add/Replace Target Skill Set (comma-separated)", placeholder="Python, SQL, ML")

email_address = st.text_input("Enter email to receive report (optional)")

if uploaded_file and job_description:
    resume_text, skills, experience = extract_info(uploaded_file)
    
    st.subheader("Extracted Resume Information")
    st.markdown("**Skills:**")
    st.write(", ".join(skills))
    st.markdown("**Experience Snippet:**")
    st.write(experience[:500] + "...")

    target_skills = [s.strip() for s in custom_skills.split(",")] if custom_skills else None
    score = match_resume_to_job(resume_text, job_description, target_skills)

    st.metric("Relevancy Score", f"{score:.2f}%")

    pdf_path = generate_pdf_report(uploaded_file.name, score, skills, experience)
    log_to_db(uploaded_file.name, score, ", ".join(skills), experience[:200])

    st.success("PDF report generated.")
    with open(pdf_path, "rb") as f:
        st.download_button("Download PDF Report", f, file_name=os.path.basename(pdf_path))

    if email_address:
        if send_email(email_address, pdf_path):
            st.success(f"Report emailed to {email_address}")
        else:
            st.error("Email sending failed.")

if st.button("Export Logs as CSV"):
    csv_path = export_logs()
    with open(csv_path, "rb") as f:
        st.download_button("Download Logs", f, file_name="resume_logs.csv")

if st.button("Show Historical Scores"):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM logs", conn)
    st.line_chart(df.set_index("timestamp")["score"])
    conn.close()
