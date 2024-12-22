# mailerlite_integration/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from django.conf import settings
from .mailerlite import MailerLiteClient

print("MailerLite Integration: Loading signals")

User = apps.get_model('givers', 'User')


@receiver(post_save, sender=User)
def add_user_to_mailerlite(sender, instance, created, **kwargs):
    print(f"Signal triggered for user: {instance.email}")
    if created:
        try:
            client = MailerLiteClient()
            name = f"{instance.first_name} {instance.last_name}".strip()

            result = client.add_subscriber(
                email=instance.email,
                name=name,
                group_id=getattr(settings, 'MAILERLITE_DEFAULT_GROUP_ID', None)
            )
            print(f"MailerLite API Response: {result}")
        except Exception as e:
            print(f"Error in MailerLite sync: {str(e)}")
