from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email',
                    'is_staff', 'is_active', 'date_joined']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(UserSkills)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(UserCauses)
class UserCausesAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(UserCharitySupport)
class UserCharitySupportAdmin(admin.ModelAdmin):
    list_display = ['user', 'charity']


@admin.register(UsersCharityOwnEvent)
class UsersCharityOwnEventAdmin(admin.ModelAdmin):
    list_display = ['user', 'name']


@admin.register(UsersPledgeOrganizations)
class UserPledgeOrganizationsAdmin(admin.ModelAdmin):
    list_display = ['user']
