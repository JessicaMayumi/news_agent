import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


def send_email(subject: str, plain_body: str, html_body: str | None = None) -> None:
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    user = os.environ["SMTP_USER"]
    pwd = os.environ["SMTP_PASSWORD"]
    to = os.environ["EMAIL_TO"]
    from_name = os.getenv("SMTP_FROM_NAME", "News Agent")

    msg = MIMEMultipart("alternative")
    msg["From"] = formataddr((from_name, user))
    msg["To"] = to
    msg["Subject"] = subject

    msg.attach(MIMEText(plain_body, "plain", "utf-8"))
    if html_body:
        msg.attach(MIMEText(html_body, "html", "utf-8"))

    if smtp_port == 465:
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=ctx, timeout=30) as s:
            s.login(user, pwd)
            s.send_message(msg)
    else:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as s:
            s.starttls()
            s.login(user, pwd)
            s.send_message(msg)
