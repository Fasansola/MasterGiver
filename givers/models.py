from django.db import models
from django.contrib.auth.models import AbstractUser
from organizations.models import Charity, PledgeOrganizations
from causes.models import Causes
from django.utils import timezone


# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    user_terms = models.BooleanField(default=True)
    state = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    country = models.CharField(max_length=128, default='United States')
    profile_photo = models.FileField(
        null=True, blank=True, upload_to='images/', default='images/upload.svg')
    about_me = models.TextField(null=True, blank=True)
    giving_motivation = models.TextField(null=True, blank=True)
    supported_charities = models.ManyToManyField(
        Charity, through='UserCharitySupport', related_name='supporting_users')

    def delete(self, *args, **kwargs):
        # Delete related objects
        self.userskills_set.all().delete()
        self.usercharitysupport_set.all().delete()
        # Call the "real" delete() method
        super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return self.username

    class Meta:
        ordering = ['username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Skill(models.Model):
    name = models.CharField(max_length=128)
    icon = models.FileField(null=True, upload_to='images/', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'


class UserSkills(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_skills')
    skill = models.ManyToManyField(Skill)

    def __str__(self):
        return f"{self.user.username} has {self.skill.name} as a skill"

    class Meta:
        ordering = ['user']
        verbose_name = 'User Skill'
        verbose_name_plural = 'User Skills'


class UserCauses(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_causes')
    cause = models.ManyToManyField(Causes)

    def __str__(self):
        return f"{self.user.username} supports {self.cause.name}"

    class Meta:
        ordering = ['user']
        verbose_name = 'User Cause'
        verbose_name_plural = 'User Causes'


class UsersCharityOwnEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} supported {self.name}"

    class Meta:
        ordering = ['user']
        verbose_name = 'User Own Event'
        verbose_name_plural = 'User Own Events'


class UsersPledgeOrganizations(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_pledge_orgs')
    pledge_organization = models.ManyToManyField(PledgeOrganizations)

    def __str__(self):
        return f"{self.user} supports {self.pledge_organization}"

    class Meta:
        ordering = ['user']
        verbose_name = 'User Pledge.to Organization'
        verbose_name_plural = 'Pledge.to Organizations Users Supports'


# NOT IN USE CURRENTLY
class UserCharitySupport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    support_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user} supports {self.charity}"

    class Meta:
        ordering = ['user']
        verbose_name = 'User Charity Support'
        verbose_name_plural = 'Charities Users Supports'
