from django.db.models import Model
from django.db.models import CharField, DateTimeField


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
