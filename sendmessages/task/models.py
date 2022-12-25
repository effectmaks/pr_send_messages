from django.db.models import Model
from django.db.models import ForeignKey, CASCADE  # связь таблиц
from django.db.models import CharField, DateTimeField, BooleanField


class Task(Model):
    """
    Модель с задачами рассылки
    """
    startdatetime = DateTimeField()  # дата и время запуска рассылки
    endtdatetime = DateTimeField()  # дата и время окончания рассылки
    message = CharField(max_length=500, default='')  # текст сообщения для доставки клиенту
    filter = CharField(max_length=100, default='')  # фильтр свойств клиентов
    status = CharField(max_length=20, default='')  # часовой пояс
    status_text = CharField(max_length=500, default='')  # текст к статусу


class Message(Model):
    """
    Модель с созданными(отправленными) сообщениями
    """
    sentdatetime = DateTimeField()  # дата и время создания
    status = BooleanField(max_length=20, default=False)  # статус отправлено
    task = ForeignKey('Task', default=None, on_delete=CASCADE, related_name='tasks')  # id рассылки
    client = ForeignKey('client.Client', default=None, on_delete=CASCADE, related_name='clients')  # id клиента

