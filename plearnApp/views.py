from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from .models import Task
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, SignInForm
from datetime import datetime
from django.utils.timezone import make_aware

naive_datetime = datetime.now()
aware_datetime = make_aware(naive_datetime)

def addTask(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user  # Set the owner to the logged-in user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()

    return render(request, 'PlearnApp/addTask.html', {'form': form})

def task_list(request):
    addedTasks = Task.objects.all()
    return render(request, "PlearnApp/task_list.html")


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = SignUpForm()
    return render(request, 'PlearnApp/sign_up.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')
    else:
        form = SignInForm()
    return render(request, 'PlearnApp/sign_in.html', {'form': form})

def sign_out(request):
    logout(request)
    return redirect('sign_in')

def dashboard(request):
    tasks = Task.objects.filter(due_date_time__gte=datetime.now()).order_by('due_date_time')
    return render(request, 'PlearnApp/dashboard.html', {'tasks': tasks})