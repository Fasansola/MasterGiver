from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class Command(BaseCommand):
    help = 'Recreate missing content types'

    def handle(self, *args, **options):
        ContentType.objects.all().delete()
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                ContentType.objects.get_or_create(
                    app_label=model._meta.app_label,
                    model=model._meta.model_name
                )
        self.stdout.write(self.style.SUCCESS(
            'Successfully recreated content types'))
