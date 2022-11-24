from django.contrib import admin

from . import models

# Tabular inline class allows edit of Group Members from admin page
class GroupMemberInline(admin.TabularInline):
    model = models.GroupMember

admin.site.register(models.Group)
