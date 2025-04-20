from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta

def default_due_date():
    return now() + timedelta(days=1)


PRIORITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]
COMPLETION_CHOICES = [
    ('0%', 'Not started'),
    ('25%', 'Just started'),
    ('50%', 'Half-way done'),
    ('75%', 'Almost done'),
    ('100%', 'Completed'),
]
REPEAT_CHOICES = [
    ('Once', 'Once'),
    ('Daily', 'Daily'),
    ('Weekly', 'Weekly'),
    ('Monthly', 'Monthly'),
]
# Task Categories
class TaskCategory(models.Model):
    Category = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.Category

# Main Task Model
class Task(models.Model):
    title = models.CharField(max_length=100)  # Task title
    description = models.TextField(max_length= 300, blank=True, null=True)  # Task description
    due_date = models.DateTimeField(default=default_due_date)#due in 24hrs if due date not added  
    completed = models.CharField(max_length=4, choices=COMPLETION_CHOICES, default='0%')  # Completion status
    priority = models.CharField(max_length=50,choices= PRIORITY_CHOICES, default= 'Low')  # Priority level
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Task owner
    task_id = models.AutoField(primary_key=True)  # Unique task ID
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, null=True, blank=True)  # Category
    notified = models.BooleanField(default=False)  # task with sent notification
    repeat = models.CharField(max_length=10, choices=REPEAT_CHOICES, default='Once')

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    notify_email = models.BooleanField(default=True)  # Email notifications enabled by default
    notify_push = models.BooleanField(default=True)   # Push notifications enabled by default

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Goal(models.Model):
    """
    Represents a goal with a title and an owner.
    """
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Milestone(models.Model):
    """
    Represents a milestone associated with a goal.
    """
    
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='milestones')
    milestone = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.milestone} (Goal: {self.goal.title})"