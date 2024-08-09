from django.db import models

# Create your models here.


class Charity(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    ngo_id = models.CharField(
        max_length=32, null=True, unique=True, blank=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    website = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
