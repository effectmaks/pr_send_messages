from rest_framework.views import APIView
from .models import Task
from .serializers import TaskCreateSerializer
from rest_framework.generics import CreateAPIView


class TaskCreate(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer

