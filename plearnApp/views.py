from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm, TaskCategoryForm, SignUpForm, SignInForm, GoalForm, MilestoneForm
from .models import Task, TaskCategory, Goal, Milestone
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils.timezone import make_aware
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import send_welcome_email
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from celery import shared_task
from django.utils.timezone import now, timedelta
from .models import Task, Milestone
from django.http import JsonResponse
from .models import Goal
from django.views.decorators.http import require_http_methods

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
import json
from .models import Milestone

# Convert naive datetime to aware datetime
naive_datetime = datetime.now()
aware_datetime = make_aware(naive_datetime)

# Landing Page
def landing_page(request):
    """
    Redirects the user to the appropriate page based on their authentication status.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('sign_in')

# Sign-Up View
def sign_up(request):
    """
    Handles user registration.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Send welcome email
            send_welcome_email(user.email, user.username)
            return redirect('dashboard')
        else:
            # Form is invalid, display errors
            return render(request, 'PlearnApp/sign_up.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'PlearnApp/sign_up.html', {'form': form})

# Sign-In View
def sign_in(request):
    """
    Handles user authentication.
    """
    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = SignInForm()
    return render(request, 'PlearnApp/sign_in.html', {'form': form})

# Sign-Out View
def sign_out(request):
    """
    Logs out the currently logged-in user and redirects to the sign-in page.
    """
    logout(request)
    return redirect('sign_in')

# Dashboard View
from django.utils.timezone import now

@login_required
def dashboard(request):
    """
    Displays the dashboard with tasks categorized into due and upcoming tasks.
    """
    tasks = Task.objects.all()  # Fetch all tasks
    milestones = Milestone.objects.all()  # Fetch all milestones
    # Tasks that are already due
    due_tasks = Task.objects.filter(owner=request.user, due_date__lte=now(), completed=False).order_by('-due_date')

    # Upcoming tasks
    upcoming_tasks = Task.objects.filter(owner=request.user, due_date__gte=now()).order_by('due_date')

    context = {
        'tasks': tasks,
        'milestones': milestones,
        'due_tasks': due_tasks,
        'upcoming_tasks': upcoming_tasks,
        'now': now(), }


    return render(request, 'PlearnApp/dashboard.html', context)

# Task List View
@login_required
def task_list(request):
    """
    Displays a list of all tasks for the logged-in user.
    """
    tasks = Task.objects.filter(owner=request.user)

    return render(request, 'PlearnApp/task_list.html', {'tasks': tasks})


# Add Task View
@login_required
def addtask(request):
    """
    Handles the creation of a new task.
    """
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user  # Set the owner to the logged-in user
            task.save()
            return redirect('dashboard')  # Redirect to the dashboard
    else:
        form = TaskForm()
    return render(request, 'PlearnApp/addtask.html', {'form': form})

# Add Category View
@login_required
def add_category(request):
    """
    Handles the creation of a new task category.
    """
    if request.method == 'POST':
        category_form = TaskCategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return redirect('addtask')  # Redirect back to the add task page
    else:
        category_form = TaskCategoryForm()
    return render(request, 'PlearnApp/add_category.html', {'category_form': category_form})



# Update Notifications View
@login_required
def update_notifications(request):
    """
    Updates the user's notification preferences.
    """
    if request.method == 'POST':
        user_profile = request.user.userprofile
        user_profile.notify_via_email = 'notify_via_email' in request.POST
        user_profile.notify_via_push = 'notify_via_push' in request.POST
        user_profile.save()
        return redirect('dashboard')  # Redirect back to the dashboard
    

# goal and milestone

@login_required
def add_goal(request):
    """
    View to add a new goal.
    """
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.owner = request.user
            goal.save()
            return redirect('goal_list')  # Redirect to the goal list view
    else:
        form = GoalForm()
    return render(request, 'PlearnApp/add_goal.html', {'form': form})


@login_required
def add_milestone(request, goal_id):
    """
    View to add a milestone to a specific goal.
    """
    goal = get_object_or_404(Goal, id=goal_id, owner=request.user)
    if request.method == 'POST':
        form = MilestoneForm(request.POST)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.goal = goal
            milestone.save()
            return redirect('goal_detail', goal_id=goal.id)  # Redirect to the goal detail view
    else:
        form = MilestoneForm()
    return render(request, 'PlearnApp/add_milestone.html', {'form': form, 'goal': goal})


@login_required
def goal_list(request):
    """
    View to display all goals for the logged-in user.
    """
    goals = Goal.objects.filter(owner=request.user)
    for goal in goals:
        total_milestones = goal.milestones.count()
        completed_milestones = goal.milestones.filter(completed=True).count()
        goal.completed_percentage = (
            int((completed_milestones / total_milestones) * 100) if total_milestones > 0 else 0
        )
    return render(request, 'PlearnApp/goal_list.html', {'goals': goals})


@login_required
def goal_detail(request, goal_id):
    """
    View to display the details of a specific goal, including its milestones.
    """
    goal = get_object_or_404(Goal,id=goal_id, owner=request.user)
    milestones = goal.milestones.all()
    return render(request, 'PlearnApp/goal_detail.html', {'goal': goal, 'milestones': milestones})


@require_POST
def toggle_completion(request, milestone_id):
    try:
        milestone = get_object_or_404(Milestone, id=milestone_id)
        
        # Parse JSON data safely
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
        
        # Ensure 'completed' is a boolean
        milestone.completed = bool(data.get("completed", False))
        milestone.save()

        return JsonResponse({"success": True, "completed": milestone.completed})
    
    except Exception as e:
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)
    



import logging
logger = logging.getLogger(__name__)


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def delete_goal(request, goal_id):
    if request.method == 'DELETE':
        try:
            logger.debug(f"Attempting to delete goal with ID: {goal_id} for user: {request.user}")
            goal = get_object_or_404(Goal, id=goal_id, owner=request.user)  # Ensure the goal belongs to the user
            goal.delete()
            logger.info(f"Goal with ID: {goal_id} successfully deleted.")
            return JsonResponse({'success': True}, status=204)
        except Goal.DoesNotExist:
            logger.error(f"Goal with ID: {goal_id} not found for user: {request.user}")
            return JsonResponse({'error': 'Goal not found'}, status=404)
        except Exception as e:
            logger.exception(f"An unexpected error occurred while deleting goal with ID: {goal_id}")
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)
    logger.warning(f"Invalid request method: {request.method} for delete_goal")
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def update_completion(request, task_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            completion = data.get('completion')
            task = Task.objects.get(pk=task_id)
            task.completed = completion
            task.save()
            return JsonResponse({'completion': task.completed})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
    return JsonResponse({'error': 'Invalid method'}, status=400)

import logging
logger = logging.getLogger(__name__)


@login_required
@csrf_exempt
def TaskDeleteView(request, task_id):
    if request.method == 'DELETE':
        try:
            logger.debug(f"Attempting to delete task with ID: {task_id} for user: {request.user}")
            task = get_object_or_404(Task, task_id=task_id, owner=request.user)  # Ensure the task belongs to the user
            task.delete()
            logger.info(f"Task with ID: {task_id} successfully deleted.")
            return JsonResponse({'success': True}, status=204)
        except Task.DoesNotExist:
            logger.error(f"Task with ID: {task_id} not found for user: {request.user}")
            return JsonResponse({'error': 'Task not found'}, status=404)
        except Exception as e:
            logger.exception(f"An unexpected error occurred while deleting task with ID: {task_id}")
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)
    logger.warning(f"Invalid request method: {request.method} for TaskDeleteView")
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def edit_task(request, task_id):
    """
    Handles editing an existing task.
    """
    task = get_object_or_404(Task, task_id=task_id, owner=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Redirect to the task list after saving
    else:
        form = TaskForm(instance=task)  # Pre-fill the form with the task's details

    return render(request, 'PlearnApp/addtask.html', {'form': form, 'task': task, 'is_edit': True})




@shared_task
def handle_repeating_tasks():
    """
    Create new tasks for tasks that are set to repeat.
    """
    tasks = Task.objects.filter(repeat__in=['Daily', 'Weekly', 'Monthly'], completed='100%')

    for task in tasks:
        if task.repeat == 'Daily':
            new_due_date = task.due_date + timedelta(days=1)
        elif task.repeat == 'Weekly':
            new_due_date = task.due_date + timedelta(weeks=1)
        elif task.repeat == 'Monthly':
            new_due_date = task.due_date + timedelta(days=30)  # Approximation for a month

        # Create a new task with the updated due date
        Task.objects.create(
            title=task.title,
            description=task.description,
            due_date=new_due_date,
            priority=task.priority,
            owner=task.owner,
            category=task.category,
            repeat=task.repeat,
        )

        # Mark the original task as non-repeating
        task.repeat = 'Once'
        task.save()