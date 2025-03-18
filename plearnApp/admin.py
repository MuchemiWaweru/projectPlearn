from django.contrib import admin
from .models import Task, TaskCategory, SubTask

admin.site.register(Task)
admin.site.register(TaskCategory)
admin.site.register(SubTask)
