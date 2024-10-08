# Generated by Django 5.0.7 on 2024-08-16 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Charity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('ngo_id', models.CharField(blank=True, db_index=True, max_length=32, null=True, unique=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('website', models.URLField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
