# Generated by Django 5.0.7 on 2024-08-18 02:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('causes', '0003_alter_causes_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='causes',
            name='icon',
            field=models.FileField(upload_to='images/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'svg'])]),
        ),
    ]