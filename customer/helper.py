from django.core.mail import send_mail
from django.conf import settings
import uuid

def send_reset_pw_mail(email):
    token = str(uuid.uuid4())
    subject = 'Your reset password link'
    message = f'Hi, click on the link to reset your password http://127.0.0.1:8000/reset-password/{token}'
    email_from  = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True