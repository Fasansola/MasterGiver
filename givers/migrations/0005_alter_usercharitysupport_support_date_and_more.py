# Generated by Django 5.0.7 on 2024-08-22 23:01

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('givers', '0004_alter_skill_icon'),
        ('organizations', '0003_pledgeorganizations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercharitysupport',
            name='support_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.RemoveField(
            model_name='userskills',
            name='skill',
        ),
        migrations.CreateModel(
            name='UsersCharityOwnEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UsersPledgeOrganizations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pledge_organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.pledgeorganizations')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Pledge.to Organization',
                'verbose_name_plural': 'Pledge.to Organizations Users Supports',
                'ordering': ['user'],
            },
        ),
        migrations.AddField(
            model_name='userskills',
            name='skill',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='givers.skill'),
        ),
    ]
