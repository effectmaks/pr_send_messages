from rest_framework.views import APIView
from .models import Task
from .serializers import TaskCreateSerializer
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView


class TaskCreate(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer


class TaskUpdate(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    lookup_field = 'id'


class TaskDelete(DestroyAPIView):
    queryset = Task.objects.all()
    lookup_field = 'id'