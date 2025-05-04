import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from app.services.loggerService import LoggerService

logger = LoggerService()

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
        self.sender_email = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_APP_PASSWORD")

        if not self.sender_email or not self.password:
            logger.warning("Email credentials not properly configured in environment variables")

    def send_email(self, recipient_email, subject, message, html_content=None):
        """
        Send an email to the specified recipient

        Args:
            recipient_email: Email address of the recipient
            subject: Email subject
            message: Plain text message body
            html_content: Optional HTML content for the email

        Returns:
            tuple: (success boolean, message string)
        """
        try:
            if not self.sender_email or not self.password:
                return False, "Email service is not configured properly"

            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))

            if html_content:
                msg.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.send_message(msg)

            logger.success(f"Email sent successfully to {recipient_email}")
            return True, "Email sent successfully"

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False, f"Failed to send email: {str(e)}"
