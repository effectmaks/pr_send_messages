from django.db.models import Model
from django.db.models import CharField, IntegerField


class Client(Model):
    """
    Модель с задачами рассылки
    """
    phone = CharField(max_length=100, default='')  # номер телефона
    code = CharField(max_length=100, default='')  # код мобильного оператора
    tag = CharField(max_length=2000, default='')  # произвольная метка
    utc = IntegerField(default=0)  # часовой пояс
