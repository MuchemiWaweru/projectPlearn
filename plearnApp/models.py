from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.timezone import now

# Task Categories
class TaskCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Main Task Model
class Task(models.Model):
    title = models.CharField(max_length=200)
    due_date_time = models.DateTimeField()
    priority = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Subtask Model
class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)  # Status of the subtask
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} - {self.title}"

def add_task(request):
    from .models import Task

    if request.method == "POST":
        title = request.POST.get('title')
        due_date_time = request.POST.get('due_date_time')
        priority = request.POST.get('priority')

        # Create and save the task
        task = Task(
            title=title,
            due_date_time=due_date_time,
            priority=priority,
            owner=request.user  # Assuming the user is logged in
        )
        task.save()
        return redirect('dashboard')  # Redirect to the dashboard or another page

    return render(request, 'PlearnApp/add_task.html')

def dashboard(request):
    # Fetch all tasks for the logged-in user, sorted by due date
    tasks = Task.objects.filter(owner=request.user).order_by('due_date_time')
    return render(request, 'PlearnApp/dashboard.html', {'tasks': tasks})
