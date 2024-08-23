from django.contrib import admin
from .models import Causes

# Register your models here.


@admin.register(Causes)
class CausesAdmin(admin.ModelAdmin):
    list_display = ['name']

# TOO COMPLEX OF A PROCESS FOR NOW

# @admin.register(MemberCause)
# class MemberCauseAdmin(admin.ModelAdmin):
#     list_display = ['cause', 'content_type', 'object_id']


# admin.site.register(Causes)
# admin.site.register(MemberCause)
