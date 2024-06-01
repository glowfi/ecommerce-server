import os
from dotenv import find_dotenv, load_dotenv
from typing import List
from pydantic import BaseModel
from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP

# Load dotenv
load_dotenv(find_dotenv(".env"))

HOST = os.getenv("MAIL_HOST")
USERNAME = os.getenv("MAIL_USERNAME")
EMAIL = os.getenv("MAIL_EMAIL")
PASSWORD = os.getenv("MAIL_PASSWORD")
PORT = os.getenv("MAIL_PORT")


class MailBody(BaseModel):
    to: List[str]
    subject: str
    body: str


def send_mail(data: dict | None = None):
    print("Entered!")
    msg = MailBody(**data)
    message = MIMEText(msg.body, "html")
    message["From"] = str(EMAIL) + "@resend.com"
    message["To"] = ",".join(msg.to)
    message["Subject"] = msg.subject

    ctx = create_default_context()

    try:
        with SMTP(HOST, PORT) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(EMAIL, PASSWORD)
            server.send_message(message)
            server.quit()
            print("Mail Send!")
        return {"status": 200, "errors": None}
    except Exception as e:
        print("Error Occured!", e)
        return {"status": 500, "errors": e}
