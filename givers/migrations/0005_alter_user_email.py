# Generated by Django 5.0.7 on 2024-08-10 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('givers', '0004_user_user_terms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
