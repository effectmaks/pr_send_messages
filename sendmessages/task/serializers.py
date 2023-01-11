from .models import Task
from rest_framework.serializers import HyperlinkedModelSerializer


class TaskCreateSerializer(HyperlinkedModelSerializer):
    """
    Cериалайзер для добавление новой рассылки
    """
    class Meta:
        model = Task
        fields = ['startdatetime', 'endtdatetime', 'message', 'filter', ]
