from django.contrib import admin
from .models import Tasks

# Register your models here.

@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_filter = ("detection_type", "hasChanged", "date_added", "date_updated")