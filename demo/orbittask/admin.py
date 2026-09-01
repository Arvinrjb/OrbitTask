from django.contrib import admin
from orbittask.models import Task, Logs


@admin.register(Task)
class AdminTask(admin.ModelAdmin):
    list_display = [
        "name", 
        "status", 
        "retries", 
        "max_retries", 
        "created_at"
    ]
    search_fields = [
        "name",
        "created_at"
    ]
    list_filter = [
        "name",
        "status",
        "created_at"
    ]

@admin.register(Logs)
class AdminTask(admin.ModelAdmin):
    list_display = [
        "task", 
        "level", 
    ]
    search_fields = [
        "name",
        "created_at",
        "finished_at"
    ]
    list_filter = [
        "task",
        "level",
        "created_at",
        "finished_at"
    ]
