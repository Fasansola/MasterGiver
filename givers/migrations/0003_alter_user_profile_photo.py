# Generated by Django 5.0.7 on 2024-11-30 21:24

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('givers', '0002_givingstyle_alter_user_profile_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.FileField(blank=True, default='images/upload.svg', null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to='images/'),
        ),
    ]
