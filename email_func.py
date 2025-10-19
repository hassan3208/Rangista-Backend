import os
import smtplib
from email.message import EmailMessage
import pathlib
import logging

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASS = os.getenv("GMAIL_APP_PASS")

# Set up logging
logger = logging.getLogger(__name__)

def send_welcome(to_email: str, to_name: str):
    if not GMAIL_USER or not GMAIL_APP_PASS:
        logger.error("GMAIL_USER or GMAIL_APP_PASS not set")
        return  # Let signup proceed without failing

    msg = EmailMessage()
    msg["Subject"] = "Welcome to Rangista — Thanks for signing up!"
    msg["From"] = f"Rangista <{GMAIL_USER}>"
    msg["To"] = to_email

    # Load HTML template, inject name, and set plain-text fallback
    template_path = pathlib.Path(__file__).with_name("welcome.html")
    try:
        html_content = template_path.read_text(encoding="utf-8")
        html_rendered = html_content.replace("{{user_name}}", to_name)
    except Exception as e:
        logger.warning(f"Failed to load welcome.html: {e}")
        html_rendered = f"<p>Hi {to_name},</p><p>Welcome to Rangista! We're glad you joined.</p><p>— Team Rangista</p>"

    # Plain text fallback
    plain_text = f"Hi {to_name},\n\nWelcome to Rangista! We're glad you joined.\n\n— Team Rangista"
    msg.set_content(plain_text)
    msg.add_alternative(html_rendered, subtype="html")

    # Connect to Gmail SMTP with STARTTLS
    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(GMAIL_USER, GMAIL_APP_PASS)
            smtp.send_message(msg)
        logger.info(f"Welcome email sent to {to_email}")
    except (smtplib.SMTPException, ConnectionError, TimeoutError) as e:
        logger.error(f"Failed to send welcome email to {to_email}: {e}")
        # Don't raise, let signup succeed