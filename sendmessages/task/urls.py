from rest_framework import routers
from django.urls import path
from .views import TaskCreate, TaskUpdate, TaskDelete


urlpatterns = [
   path('tasks/', TaskCreate.as_view(), name='task_create'),
   path('tasks/<int:id>/', TaskUpdate.as_view(), name='task_update'),
   path('tasks/delete/<int:id>/', TaskDelete.as_view(), name='task_delete'),
]
