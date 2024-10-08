from django.contrib import admin
from .models import Charity, PledgeOrganizations

# Register your models here.


@admin.register(Charity)
class CharityAdmin(admin.ModelAdmin):
    list_display = ['name', 'ngo_id', 'website']


@admin.register(PledgeOrganizations)
class PledgeOrganizationsAdmin(admin.ModelAdmin):
    list_display = ['id']
