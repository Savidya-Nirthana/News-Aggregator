from dotenv import load_dotenv
import os 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_HOST")
        self.smtp_port = os.getenv("SMTP_PORT")
        self.username = os.getenv("SMTP_USER")
        self.password = os.getenv("SMTP_PASS")

    def send_email(self, to_address: str, subject: str, body: str):
        msg = MIMEMultipart()
        msg['from'] = self.username
        msg['to'] = to_address
        msg['subject'] = subject
        msg.attach(MIMEText(body, 'plain'))


        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)


email_service = EmailService()
email_service.send_email("snirthana1@gmail.com", "Test Subject", "Test Body")