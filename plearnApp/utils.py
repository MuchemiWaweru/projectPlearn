from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime

def send_welcome_email(user_email, username):
    subject = "Welcome to Plearn!"
    message = f"Hi {username},\n\nThank you for signing up for Plearn. We're excited to have you on board!\n\nBest regards,\nPlearn \nby LooksMatt"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)

def swahili_greeting():
    """
    Returns a Swahili greeting based on the time of day.
    """
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        return "Habari za asubuhi"  
    elif 12 <= current_hour < 17:
        return "Habari za mchana"  
    elif 17 <= current_hour < 20:
        return "Habari za jioni"  
    else:
        return "Habari za usiku"  