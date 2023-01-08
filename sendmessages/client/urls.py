from rest_framework import routers
from django.urls import path
from .views import ClientList, ClientUpdate


urlpatterns = [
   path('clients', ClientList.as_view(), name='clients'),
   path('clients/<int:id>/', ClientUpdate.as_view(), name='client_update'),
]
