from django.urls import path

# Create your views here.
from .import views

urlpatterns = [
   path('', views.view_list, name='view_list')
]
