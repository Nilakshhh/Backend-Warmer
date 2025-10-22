import requests
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# --- Config ---
load_dotenv()

URL = os.getenv("URL")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")


def ping_and_email():
    status = ""
    resp = ""
    try:
        resp = requests.get(URL, timeout=10)
        status = f"✅ {URL} responded with {resp.status_code}\n\n{resp.text}"
    except Exception as e:
        status = f"❌ {URL} request failed:\n{e}"
    print(status)
    print(resp)
    # prepare email
    msg = MIMEText(status)
    msg["Subject"] = "Backend Health Check"
    msg["From"] = EMAIL_USER
    msg["To"] = TO_EMAIL

    # send email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

if __name__ == "__main__":
    ping_and_email()
