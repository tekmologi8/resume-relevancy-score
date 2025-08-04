import smtplib
from email.message import EmailMessage

def send_email(to_address, file_path):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Resume Analysis Report"
        msg["From"] = "your-email@example.com"
        msg["To"] = to_address

        msg.set_content("Attached is your resume analysis report.")
        with open(file_path, "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=os.path.basename(file_path))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("your-email@example.com", "your-app-password")
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("Email error:", e)
        return False
