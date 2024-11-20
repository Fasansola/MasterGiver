from django.core.management.base import BaseCommand
import smtplib
from email.mime.text import MIMEText
from django.conf import settings

class Command(BaseCommand):
    help = 'Test SMTP email connection'

    def handle(self, *args, **options):
        smtp_server = "smtp-relay.brevo.com"
        port = 587
        sender = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD
        recipient = "wpxstudiox@gmail.com"

        try:
            self.stdout.write(f"Testing with {smtp_server}")
            self.stdout.write(f"Using credentials:")
            self.stdout.write(f"Email: {sender}")
            self.stdout.write(f"Password length: {len(password) if password else 'None'}")
            
            server = smtplib.SMTP(smtp_server, port)
            server.set_debuglevel(1)
            server.starttls()
            
            self.stdout.write("Attempting login...")
            server.login(sender, password)
            self.stdout.write(self.style.SUCCESS("Login successful!"))
            
            msg = MIMEText('Test message')
            msg['Subject'] = 'Test Subject'
            msg['From'] = sender
            msg['To'] = recipient
            
            self.stdout.write("Sending email...")
            server.send_message(msg)
            self.stdout.write(self.style.SUCCESS("Email sent successfully!"))
            
            server.quit()
            return True
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
            if hasattr(e, 'smtp_error'):
                self.stdout.write(self.style.ERROR(f"SMTP Error: {str(e.smtp_error)}"))
            return False