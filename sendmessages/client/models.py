from django.db.models import Model
from django.db.models import CharField


class Client(Model):
    """
    Модель с задачами рассылки
    """
    phone = CharField(max_length=100, default='')  # номер телефона
    code = CharField(max_length=100, default='')  # код мобильного оператора
    tag = CharField(max_length=2000, default='')  # произвольная метка
    status = CharField(max_length=20, default='')  # часовой пояс
    status_text = CharField(max_length=500, default='')  # текст к статусу
