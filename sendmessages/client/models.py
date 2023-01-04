from django.db.models import Model
from django.db.models import CharField, IntegerField


class Client(Model):
    """
    Модель с задачами рассылки
    """
    phone = CharField(max_length=100, blank=False, default='')  # номер телефона
    code = CharField(max_length=100, blank=False,  default='')  # код мобильного оператора
    tag = CharField(max_length=2000, blank=False,  default='')  # произвольная метка
    utc = IntegerField(blank=False, default=0)  # часовой пояс
