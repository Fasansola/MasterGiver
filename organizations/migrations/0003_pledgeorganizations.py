# Generated by Django 5.0.7 on 2024-08-22 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_alter_charity_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='PledgeOrganizations',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
        ),
    ]
