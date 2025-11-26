"""Email sending functionality using SMTP."""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import (
    FROM_EMAIL,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USERNAME,
    TO_EMAIL,
)

logger = logging.getLogger(__name__)


def send_email(subject: str, body_plain: str, body_html: str) -> None:
    """
    Send an email via SMTP with both plain text and HTML versions.
    
    Args:
        subject: Email subject line
        body_plain: Plain text email body
        body_html: HTML email body
        
    Raises:
        Exception: If email sending fails
    """
    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = FROM_EMAIL
        msg["To"] = TO_EMAIL
        
        # Attach plain text and HTML parts
        part1 = MIMEText(body_plain, "plain")
        part2 = MIMEText(body_html, "html")
        
        msg.attach(part1)
        msg.attach(part2)
        
        # Connect to SMTP server and send
        logger.info(f"Connecting to SMTP server {SMTP_HOST}:{SMTP_PORT}...")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()  # Enable TLS encryption
            logger.info(f"Logging in as {SMTP_USERNAME}...")
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            logger.info(f"Sending email to {TO_EMAIL}...")
            server.send_message(msg)
        
        logger.info("Email sent successfully!")
        
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error while sending email: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while sending email: {e}")
        raise

