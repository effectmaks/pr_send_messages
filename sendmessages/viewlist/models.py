from django.db.models import Model
from django.db.models import CharField


class TaskList(Model):
    """
    Модель с задачами рассылки
    """
    name = CharField(max_length=100, default='')  # имя рассылки
    text_message = CharField(max_length=2000, default='')  # текст рассылки
    status = CharField(max_length=20, default='')  # статус выполнения
    status_text = CharField(max_length=500, default='')  # текст к статусу
