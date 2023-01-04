from rest_framework import routers
from django.urls import path
from .views import ClientList


urlpatterns = [
   path('clients', ClientList.as_view(), name='clients')
]
