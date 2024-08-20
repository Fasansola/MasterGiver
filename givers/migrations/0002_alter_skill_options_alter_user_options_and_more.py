# Generated by Django 5.0.7 on 2024-08-17 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('givers', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='skill',
            options={'ordering': ['name'], 'verbose_name': 'Skill', 'verbose_name_plural': 'Skills'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username'], 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AlterModelOptions(
            name='usercharitysupport',
            options={'ordering': ['user'], 'verbose_name': 'User Charity Support', 'verbose_name_plural': 'Charities Users Supports'},
        ),
        migrations.AlterModelOptions(
            name='userskills',
            options={'ordering': ['user'], 'verbose_name': 'User Skill', 'verbose_name_plural': 'User Skills'},
        ),
        migrations.AlterField(
            model_name='skill',
            name='icon',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
