import logging
from django.utils import timezone

from django.db.models import Count
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from sendmessages.celery import app
from .models import Task, Message
from client.models import Client
#https://probe.fbrq.cloud/docs
URL_SERVER_POST = 'https://probe.fbrq.cloud/v1/send/'
TIMEOUT_SERVER = 2
import requests
import json
import os


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


@app.task(name='check_new_messages')
def check_new_messages():
    """
    Проверяет наличие сообщений для отправки.
    При их наличии отправлет.
    """
    try:
        print(f'Проверить сообщения у заданий со статусом START')
        # Запрос найти задание, у которого больше всех кол-во сообщений, которые не отправлены
        task_go = Message.objects.values('task__id')\
                              .filter(task__status__in=[Task.StatusTask.START, Task.StatusTask.WORK])\
                              .filter(status=Message.StatusMessage.CREATE)\
                              .annotate(Count('status')).order_by('-status__count')[:1]
        if task_go:
            info_finded_task(task_go)
            task = Task.objects.filter(id=task_go[0].get('task__id')).first()
            start_sending(task)
    except Exception as e:
        print(f'Ошибка поиска сообщений у заданий со статусом START. {e}')


def info_finded_task(task_go):
    """
    Показать информацию какое задание требует отправки сообщений
    :param task: Задание
    :return:
    """
    task_id = task_go[0].get('task__id')
    message_count = task_go[0].get('status__count')
    print(f'Выполнить задание ID:{task_id}. Осталось сообщений:{message_count}')


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
        task_status_error(msg_err, task)


def task_status_created_ok(task):
    """
    Пометить статус к заданию - "Начать отправку"
    :param task: Задание
    """
    task.status = Task.StatusTask.START
    print(f'Задание создано для {task}')


def task_status_error(msg_err, task):
    """
    Пометить статус к заданию - "Ошибка"
    :param msg_err: Сообщение ошибки
    :param task: Задание
    """
    task.status = Task.StatusTask.ERROR
    task.status_text = msg_err
    task.save()
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
            task_status_error(msg_err, task)
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


def start_sending(task):
    """
    Начать отправку для задания.
    Отправляет только 5 сообщений.
    :param task: Задача на отправку
    """
    try:
        print(f'Начать отправку для задания {task}')
        if task.status == Task.StatusTask.START:  # Пометить что задание в работе
            label_work_task(task)
        for message in task.client_messages.filter(status=Message.StatusMessage.CREATE).all()[:5]:
            message_send(message)
        check_end_task(task)
    except Exception as e:
        print(f'Ошибка поиска сообщений у задания {task}. {e}')
        label_error_task(task, e)


def label_work_task(task):
    """
    Пометить задание статусом WORK(работа)
    :param task: Задание
    """
    print(f'Установить статус "WORK" для task {task}')
    task.status = Task.StatusTask.WORK
    task.save()


def check_end_task(task):
    """
    Проверить, что сообщений для отправки больше нет у задания.
    Пометить задание статусом END(завершена отправка)
    :param task: Задание
    """
    try:
        print(f'Проверить кол-во сообщений для отправки у задания {task}')
        task_end = Message.objects.values('task__id')\
            .filter(task__status=Task.StatusTask.WORK) \
            .filter(task__id=task.id) \
            .filter(status=Message.StatusMessage.CREATE) \
            .annotate(Count('status'))
        if task_end:
            count = task_end[0].get('status__count', -1)
            if count == 0:
                label_end_task(task)
            else:
                print(f'Осталось сообщений {count}')
        else:  # запрос ничего не вернул, значит все сообщения отработаны
            label_end_task(task)
    except Exception as e:
        print(f'Ошибка проверки завершения задания {task}. {e}')
        task_status_error({e}, task)


def label_end_task(task):
    """
    Пометить задание статусом END(завершена отправка)
    :param task: Задание
    """
    print(f'Окончена отправка для task {task}')
    task.status = Task.StatusTask.END
    task.save()


def label_error_task(task, msg):
    """
    Пометить задание статусом ERROR(ошибка)
    :param task: Задание
    :param msg: Сообщение ошибки
    """
    print(f'Ошибка task {task}')
    task.status = Task.StatusTask.ERROR
    task.status_text = msg
    task.save()


def message_send(message):
    """
    Отправить сообщение
    :param message: Сообщение
    """
    try:
        send_server_message(message)
    except Exception as e:
        print(f'Ошибка отправки сообщения у задания {task}. {e}')
        label_error_message(message)


def label_error_message(message, msg: str = ""):
    """
    Пометить сообщение статусом ERROR(ошибка отправки)
    :param message: Объект сообщения
    :param msg: Текст ответа сервера
    """
    print(f'Ошибка отправки сообщения {message}. {msg}')
    message.status = Message.StatusMessage.ERROR
    message.save()


def send_server_message(message):
    """
    Отправить серверу запрос с cобщением для клиента
    :param message: Сообщение
    """
    try:
        label_sending_message(message)
        header = {'Authorization': os.getenv('TOKEN_SECURITY')}
        body = get_parameters_request(message)
        response = requests.post(f'{URL_SERVER_POST}{message.id}', data=body, headers=header, timeout=TIMEOUT_SERVER)
        check_response_server(response, message)
    except Exception as e:
        print(f'Ошибка сервера. НЕ отправлено сообщение для клиента {message.client}.')
        label_error_message(message, msg=f'{e}')


def check_response_server(response, message):
    """
    В зависимости от ответа сервера, устанавливается статус сообщения в базе
    :param response: Ответ сервера
    """
    if 200 <= response.status_code < 400:
        label_ok_message(message, msg=f'Status_code:{response.status_code} {response.text}')
    elif response.status_code >= 400:
        label_error_message(message, msg=f'Status_code:{response.status_code} {response.text}')


def label_ok_message(message, msg: str = ""):
    """
    Пометить сообщение статусом OK(успешно отправлено)
    :param message: Объект сообщения
    :param msg: Текст ответа сервера
    """
    message.status = Message.StatusMessage.OK
    message.save()
    print(f'Отправлено сообщение для клиента {message.client}. {msg}')


def label_sending_message(message):
    """
    Пометить сообщение статусом SENDING(отправка)
    :param task: Сообщение
    """
    print(f'Отправить сообщение для клиента {message.client}')
    message.status = Message.StatusMessage.SENDING
    message.save()


def get_parameters_request(message):
    """
    Формирование параметров для запроса на сервер
    :param message: Сообщение
    :return: {параметры}
    """
    phone = f'{message.client.code}{message.client.phone}'
    params = {'id': message.id, 'phone': phone, 'text': message.task.message}
    return json.dumps(params)
