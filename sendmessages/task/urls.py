from rest_framework import routers
from django.urls import path
from .views import TaskCreate


urlpatterns = [
   path('tasks/', TaskCreate.as_view(), name='task_create'),
]
