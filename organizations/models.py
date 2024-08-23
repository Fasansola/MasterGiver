from django.db import models

# Create your models here.

# FOR MASTER GIVERS OWN CHARITY ORGANIZATIONS - CURRENTLY NOT IN USE


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
        verbose_name = 'Charity'
        verbose_name_plural = 'Charities'


#
class PledgeOrganizations(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
