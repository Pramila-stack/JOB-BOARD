# utils.py
from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_notification_email(subject, template_name, context, recipient_list):
    """
    Renders an HTML template and sends the email.
    """
    html_message = render_to_string(template_name, context)
    send_mail(
        subject=subject,
        message="Please enable HTML to view this email.", # Fallback
        from_email=None, # Uses DEFAULT_FROM_EMAIL in settings
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=False, 
    )