from django.contrib import admin
from orbittask.models import Task


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
