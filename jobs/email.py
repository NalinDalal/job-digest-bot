import os
from typing import List, Dict
from .templates import HTML_EMAIL, PLAIN_TEXT

MAIL_PROVIDER = os.getenv("MAIL_PROVIDER", "sendgrid")  # or 'gmail'

def build_email_bodies(jobs: List[Dict], date_str: str, mode: str):
    html = HTML_EMAIL.render(jobs=jobs, date_str=date_str, mode=mode)
    text = PLAIN_TEXT.render(jobs=jobs, date_str=date_str, mode=mode)
    return text, html

def send_email_sendgrid(subject: str, text: str, html: str):
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail

    api_key = os.getenv("SENDGRID_API_KEY")
    mail_from = os.getenv("MAIL_FROM")
    mail_to = os.getenv("MAIL_TO")
    if not api_key or not mail_from or not mail_to:
        raise RuntimeError("Missing SENDGRID_API_KEY / MAIL_FROM / MAIL_TO")

    message = Mail(
        from_email=mail_from,
        to_emails=mail_to,
        subject=subject,
        plain_text_content=text,
        html_content=html
    )
    sg = SendGridAPIClient(api_key)
    sg.send(message)

def send_email_gmail(subject: str, text: str, html: str):
    # Placeholder for Gmail API OAuth2 flow; recommend SendGrid for simplicity in CI.
    raise NotImplementedError("Gmail provider not implemented in CI sample. Use SendGrid or extend this function.")

def send_email(subject: str, text: str, html: str):
    if MAIL_PROVIDER == "sendgrid":
        return send_email_sendgrid(subject, text, html)
    else:
        return send_email_gmail(subject, text, html)
