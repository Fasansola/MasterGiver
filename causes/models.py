from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

# Create your models here.


class Causes(models.Model):
    name = models.CharField(max_length=64)
    icon = models.ImageField()
    color = models.CharField(max_length=9)


class MemberCause(models.Model):
    cause = models.ForeignKey(Causes, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    date_added = models.DateTimeField(default=timezone.now)
