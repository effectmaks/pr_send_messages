import logging

from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from sendmessages.celery import app


@app.task(name='print_test_work')
def print_test():
    print('Celery work!')
