from django.db.models import Model, TextChoices
from django.db.models import ForeignKey, CASCADE  # связь таблиц
from django.db.models import CharField, DateTimeField, BooleanField
from django.utils.translation import gettext_lazy as _


class Task(Model):
    """
    Модель с задачами рассылки
    """

    class StatusTask(TextChoices):
        NONE = 'NN', _('None')  # Создать
        START = 'ST', _('Start')  # Запустить
        WORK = 'WK', _('Work')  # Сообщения отправляются
        ERROR = 'ER', _('Error')  # Ошибка
        WARNING = 'WR', _('Warning')  # Требует внимания
        END = 'ED', _('End')  # Успешно завершена отправка

    startdatetime = DateTimeField(blank=False)  # дата и время запуска рассылки
    endtdatetime = DateTimeField(blank=False)  # дата и время окончания рассылки
    message = CharField(max_length=500, blank=False, default='')  # текст сообщения для доставки клиенту
    filter = CharField(max_length=100, blank=False, default='')  # фильтр свойств клиентов
    status = CharField(  # статус
        max_length=2,
        choices=StatusTask.choices,
        default=StatusTask.NONE,
    )
    status_text = CharField(max_length=500, default='')  # текст к статусу

    def __str__(self):
        return f'ID:{self.id} Status: {self.status}'


class Message(Model):
    """
    Модель с созданными(отправленными) сообщениями
    """

    class StatusMessage(TextChoices):
        CREATE = 'CR', _('Created')  # Создано
        SENDING = 'SD', _('Sending')  # Отправляет
        ERROR = 'ER', _('Error')  # Ошибка
        OK = 'OK', _('OK')  # Отправлено

    sentdatetime = DateTimeField()  # дата и время создания
    status = CharField(  # статус отправлено
        max_length=2,
        choices=StatusMessage.choices,
        default=StatusMessage.CREATE,
    )
    task = ForeignKey('Task', default=None, on_delete=CASCADE, related_name='tasks')  # id рассылки
    client = ForeignKey('client.Client', default=None, on_delete=CASCADE, related_name='clients')  # id клиента
