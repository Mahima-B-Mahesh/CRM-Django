import uuid

from .models import Students

import random

import string

# emial related imports
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def get_admission_number():

    while True:

        admission_number = f"LM-{str(uuid.uuid4().int)[:7]}"

        if not Students.objects.filter(adm_number=admission_number).exists():

            return admission_number

    # print(pattern)


get_admission_number()


def get_password():
    """
    Generates a random password.
    """
    password = "".join(random.choices(string.ascii_letters + string.digits, k=12))

    return password


get_password()

# email sending

def send_email(subject,recepient,template,context):
    """
    Sends an email with the given subject, recipient, template, and context.
    """
    html_content = render_to_string(template, context)
    msg = EmailMultiAlternatives(subject, html_content, settings.EMAIL_HOST_USER, [recepient])
    msg.attach_alternative(html_content, "text/html")
    msg.send()