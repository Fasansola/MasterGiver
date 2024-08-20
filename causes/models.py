from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from django.core.validators import FileExtensionValidator

# Create your models here.


class Causes(models.Model):
    name = models.CharField(max_length=64)
    icon = models.FileField(upload_to='images/', validators=[FileExtensionValidator(
        allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'svg'])])
    color = models.CharField(max_length=9)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Cause'
        verbose_name_plural = 'Causes'


class MemberCause(models.Model):
    cause = models.ForeignKey(Causes, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Member Cause'
        verbose_name_plural = 'Member Causes'
