import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
RESUME_FILE = os.getenv("RESUME_FILE")
EXCEL_FILE = os.getenv("EXCEL_FILE")

def send_mail(to_email, greeting, company_name):
    msg = MIMEMultipart()
    msg["Subject"] = f"Application for Software Developer Role – Nilaksh Dureja"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    # --- Email Body ---
    body = f"""\
{greeting}

I hope this email finds you well.

I am reaching out to express my interest in any suitable job opportunities at {company_name if pd.notna(company_name) else 'your organization'}. I am passionate about software development and believe my skills in Python, JavaScript, and backend development align well with your organization's goals.

Please find attached my resume for your reference. I would be grateful for the opportunity to discuss how I can contribute to your team.

Looking forward to hearing from you.

Best regards,  
Nilaksh Dureja   
https://www.linkedin.com/in/nilaksh-dureja/
"""
    msg.attach(MIMEText(body, "plain"))

    # --- Attach Resume ---
    with open(RESUME_FILE, "rb") as f:
        resume = MIMEApplication(f.read(), _subtype="pdf")
        resume.add_header("Content-Disposition", "attachment", filename="Nilaksh_Dureja_Resume.pdf")
        msg.attach(resume)

    # --- Send ---
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

    print(f"✅ Email sent to: {to_email}")

def process_excel():
    df = pd.read_excel(EXCEL_FILE)

    for _, row in df.iterrows():
        company = row.get("company_name", "")
        first = row.get("first_name", "")
        last = row.get("last_name", "")
        email = row.get("email", "")

        if not pd.notna(email) or not str(email).strip():
            print("⚠️ Skipping row with no email.")
            continue
        email_str = str(email).strip()

        # Skip if it contains multiple emails
        if " " in email_str or "," in email_str or ";" in email_str:
            print(f"⚠️ Skipping row with multiple emails: {email_str}")
            continue
        
        if pd.notna(first) and str(first).strip():
            # If first name exists → personalized
            name_part = f"{first.strip()} {last.strip()}" if pd.notna(last) and str(last).strip() else first.strip()
            greeting = f"Dear {name_part},"
        else:
            # Fallback
            greeting = "Dear Hiring Manager,"

        send_mail(email, greeting, company)

if __name__ == "__main__":
    process_excel()
