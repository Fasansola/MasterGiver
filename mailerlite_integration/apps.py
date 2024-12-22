from django.apps import AppConfig


class MailerliteIntegrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailerlite_integration'

    def ready(self):
        print("=====================================")
        print("Initializing MailerLite Integration")
        print("=====================================")
        try:
            import mailerlite_integration.signals
            print("Signals imported successfully!")
        except Exception as e:
            print(f"Error importing signals: {e}")
