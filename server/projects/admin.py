from django.contrib import admin
from .models import Projects, Task


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_completed', 'created_at', 'date_started', 'date_ended', 'owner']
    search_fields = ['name']
    list_filter = ['is_completed', 'created_at']


class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_completed', 'created_at', 'date_to_end', 'project', 'executor']
    search_fields = ['name']
    list_filter = ['is_completed', 'created_at']


admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Task, TaskAdmin)
