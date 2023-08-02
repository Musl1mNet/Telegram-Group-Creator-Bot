from django.contrib import admin

from .models import Group, TelegramUser

# Register your models here.

admin.site.register(TelegramUser)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']
