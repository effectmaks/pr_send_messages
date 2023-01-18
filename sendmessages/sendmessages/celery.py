import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sendmessages.settings')
app = Celery('sendmessages')
app.config_from_object('django.conf:settings', namespace='CELERY_')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
