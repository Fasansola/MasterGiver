from django.db import models
from django.contrib.auth.models import AbstractUser
from organizations.models import Charity


# Create your models here.
class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='givers_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='givers_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    state = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    profile_photo = models.ImageField(null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    giving_motivation = models.TextField(null=True, blank=True)
    supported_charities = models.ManyToManyField(
        Charity, through='UserCharitySupport')

    def __str__(self) -> str:
        return self.username

    class Meta:
        ordering = ['username']


class Skill(models.Model):
    name = models.CharField(max_length=128)
    icon = models.ImageField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class UserSkills(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ManyToManyField(Skill)

    def __str__(self):
        return self.user

    class Meta:
        ordering = ['user']


class UserCharitySupport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    support_date = models.DateField()

    def __str__(self):
        return f"{self.user} supports {self.charity}"
