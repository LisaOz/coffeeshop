import os
from celery import Celery

"""
This file provides Celery instance configuration for the project.
"""

# Set the default Django settings module for the celery program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffeeshop.settings')  # set variable for Celery command-line program

app = Celery('coffeeshop') # create an instance of the application

# Load any custom configuration from the project settings, Celery namespace setting is needed
app.config_from_object('django.conf:settings', namespace='CELERY')

# Tell Celery to auto-discover asynchronous tasks for the application. Celery looks for a tasks.py file
# in each app directory of apps added to INSTALLED_APP and load asynchronous tasks defined in it
app.autodiscover_tasks()
