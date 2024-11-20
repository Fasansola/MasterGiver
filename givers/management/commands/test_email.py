from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
import socket


class Command(BaseCommand):
    help = 'Test email sending configuration'

    def handle(self, *args, **options):
        try:
            # First try basic connection
            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.ehlo()
                if settings.EMAIL_USE_TLS:
                    server.starttls()
                server.ehlo()
                server.login(settings.EMAIL_HOST_USER,
                             settings.EMAIL_HOST_PASSWORD)

                # Create message
                msg = MIMEText('Test message')
                msg['Subject'] = 'Test Subject'
                msg['From'] = settings.DEFAULT_FROM_EMAIL
                msg['To'] = 'wpxstudiox@gmail.com'

                # Send message and get full response
                try:
                    server.send_message(msg)
                    return "Email test completed successfully"
                except smtplib.SMTPRecipientsRefused as e:
                    return f"Recipients refused: {str(e)}"
                except smtplib.SMTPResponseException as e:
                    return f"SMTP error occurred: {e.smtp_code} {e.smtp_error}"

        except socket.gaierror:
            return "DNS lookup failed"
        except smtplib.SMTPAuthenticationError:
            return "SMTP authentication failed"
        except Exception as e:
            return f"Error: {str(e)}"
