from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name']
    search_fields = ['email', 'first_name', 'last_name']


admin.site.register(get_user_model(), UserAdmin)
admin.site.unregister(Group)
