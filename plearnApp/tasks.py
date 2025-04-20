from celery import shared_task
from django.core.mail import send_mail
from .models import Task, Milestone
from django.utils.timezone import localdate

def get_tasks_and_milestones(user):
    """
    Retrieves tasks and milestones due today for a given user.
    """
    today = localdate()
    tasks = Task.objects.filter(due_date__date=today, completed=False, owner=user)
    milestones = Milestone.objects.filter(due_date__date=today, owner=user)
    return tasks, milestones

@shared_task
def send_daily_reminders():
    """
    Sends an email every morning to remind users of tasks and milestones due today.
    """
    users = Task.objects.values_list('owner', flat=True).distinct()
    users = set(users).union(Milestone.objects.values_list('owner', flat=True))
    
    for user_id in users:
        user = user.objects.get(id=user_id)
        tasks, milestones = get_tasks_and_milestones(user)
        
        if tasks or milestones:
            task_list = "\n".join([f"- {task.title} (Due: {task.due_date.strftime('%H:%M')})" for task in tasks])
            milestone_list = "\n".join([f"- {milestone.title} (Due: {milestone.due_date.strftime('%H:%M')})" for milestone in milestones])
            
            message = f"Hello {user.username},\n\n"
            message += "Here is your reminder for today's due tasks and milestones:\n\n"
            if tasks:
                message += "Tasks:\n" + task_list + "\n\n"
            if milestones:
                message += "Milestones:\n" + milestone_list + "\n\n"
            message += "Stay productive!\n\nBest regards,\nPlearn"
            
            send_mail(
                subject="Daily Reminder: Tasks & Milestones Due Today",
                message=message,
                from_email='noreply@plearn.com',
                recipient_list=[user.email],
                fail_silently=False,
            )



from django.utils.timezone import now, timedelta


@shared_task
def send_task_due_notifications():
    """
    Send email notifications for tasks due in less than 24 hours.
    """
    tasks = Task.objects.filter(due_date__lte=now() + timedelta(hours=24), due_date__gte=now(), notified=False)

    for task in tasks:
        send_mail(
            subject=f"Reminder: Task '{task.title}' is due soon",
            message=f"Hello,\n\nYour task '{task.title}' is due on {task.due_date}. Please make sure to complete it on time.\n\nBest regards,\nPlearn Team",
            from_email='noreply@plearn.com',
            recipient_list=[task.owner.email],
            fail_silently=False,
        )
        task.notified = True
        task.save()

@shared_task
def send_milestone_due_notifications():
    """
    Send email notifications for milestones due in less than 24 hours.
    """
    milestones = Milestone.objects.filter(due_date__lte=now() + timedelta(hours=24), due_date__gte=now(), completed=False)

    for milestone in milestones:
        send_mail(
            subject=f"Reminder: Milestone '{milestone.milestone}' is due soon",
            message=f"Hello,\n\nYour milestone '{milestone.milestone}' for the goal '{milestone.goal.title}' is due on {milestone.due_date}. Please make sure to complete it on time.\n\nBest regards,\nPlearn Team",
            from_email='noreply@plearn.com',
            recipient_list=[milestone.goal.owner.email],
            fail_silently=False,
        )