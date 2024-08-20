# Generated by Django 5.0.7 on 2024-08-18 01:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('causes', '0002_alter_causes_options_alter_membercause_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='causes',
            name='icon',
            field=models.ImageField(upload_to='images/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'svg'])]),
        ),
    ]
