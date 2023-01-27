import logging
from django.utils import timezone

from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from sendmessages.celery import app
from .models import Task, Message
from client.models import Client


@app.task(name='print_test')
def print_test():
    print('Celery work!')


@app.task(name='check_tasks')
def check_tasks():
    """
    Ищет новые задачи(создает сообщения на отправку) и закрывает просроченные
    """
    try:
        check_task_time_start()  # Проверка наличия новых задач и создание сообщений для отправки
        check_task_time_end()  # Останавливает истёкшие по времени задачи.
    except Exception as e:
        print(f'Ошибка при поиске новых и истёкших задач. {e}')


def create_messages(clients, task):
    """
    Создание сообщений для отправки
    :param clients: Клиенты
    :param task: Задание
    """
    if clients:
        for client in clients:
            # создание сообщений для клиентов
            message = Message(sentdatetime=timezone.now(),
                              task=task,
                              client=client)
            message.save()
        task_status_created_ok(task)  # Пометить статус к заданию - "Начать отправку"
    else:
        msg_err = f'Задание не запущено для task {task}. Клиентов для фильтра: {task.filter} - НЕТ!'
        task_status_created_error(msg_err, task)


def task_status_created_ok(task):
    """
    Пометить статус к заданию - "Начать отправку"
    :param task: Задание
    """
    task.status = Task.StatusTask.START
    print(f'Задание создано для {task}')


def task_status_created_error(msg_err, task):
    """
    Пометить статус к заданию - "Ошибка создания отправки"
    :param msg_err: Сообщение ошибки
    :param task: Задание
    """
    task.status = Task.StatusTask.ERROR
    task.status_text = msg_err
    print(msg_err)


def check_task_time_start():
    """
    Проверка наличия новых задач по времени старта и создание сообщений для отправки
    """
    print('Проверка наличия новых задач по времени старта и создание сообщений для отправки')
    # Поиск задач по установленному времени
    try:
        time_now = timezone.now()
        tasks = Task.objects.filter(startdatetime__lt=time_now,
                                    endtdatetime__gt=time_now,
                                    status=Task.StatusTask.NONE).all()
        loop_tasks_to_create_messages(tasks)
    except Exception as e:
        print(f'Ошибка запроса на выгрузку задач. {e}')


def loop_tasks_to_create_messages(tasks):
    """
    Перебирает лист задач и ищет клиентов по фильтру
    :param tasks: Найденные задачи
    """
    try:
        for task in tasks:
            print(f'Создание сообщений для отправки task {task}')
            find_clients_filter(task)  # По одной задаче ищет клиентов по фильтру
    except Exception as e:
        print(f'Ошибка в цикле создания сообщений. {e}')


def find_clients_filter(task):
    """
    По одной задаче ищет клиентов по фильтру
    :param task: Задача
    """
    try:
        clients = Client.objects.filter(tag=task.filter)  # поиск клиентов с тегом задачи
        try:
            create_messages(clients, task)  # Создание сообщений для отправки
        except Exception as e:
            msg_err = f'Ошибка создания сообщений для отправки. {e}'
            task_status_created_error(msg_err, task)
        task.save()
    except Exception as e:
        print(f'Ошибка запроса на выгрузку клиентов. {e}')


def check_task_time_end():
    """
    Останавливает истёкшие по времени задачи.
    Прекращается отправка сообщений.
    """
    print('Проверка и остановка задач по истёкшему времени')
    # Поиск задач по истёкшему времени
    try:
        time_now = timezone.now()
        tasks = Task.objects.filter(endtdatetime__lte=time_now,
                                    status__in=[Task.StatusTask.NONE,
                                                Task.StatusTask.START,
                                                Task.StatusTask.WORK]) \
                             .all()
        loop_task_stop(tasks)
    except Exception as e:
        print(f'Ошибка выгрузки заданий по истекшему времени. {e}')
        for_debug_sql()


def loop_task_stop(tasks):
    """
    Перебирает истекшие задания и выставляет статус END
    :param tasks: Задачи, которые нужно остановить
    """

    try:
        for task in tasks:
            print(f'Остановить задание по истёкшему времени task {task}')
            task.status = Task.StatusTask.END
            task.save()
    except Exception as e:
        print(f'Ошибка установки статуса END. {e}')


def for_debug_sql():
    """
    DEBUG
    Пишет в celery какие запросы отправляет в базу данных.
    """
    from django.db import connection
    print(connection.queries)
    from django.db import reset_queries
    reset_queries()
