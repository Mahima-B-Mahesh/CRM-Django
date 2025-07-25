"""
WSGI config for crm project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from Payments.cron import scheduler_start

scheduler_start()  # Start the scheduler for sending remainder emails

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')

application = get_wsgi_application()
