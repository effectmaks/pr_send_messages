from django.test import TestCase
from ..models import Task, Message
from ..tasks import check_new_messages, check_tasks
from django.apps import apps
from django.utils import timezone
from datetime import timedelta


class TasksTest(TestCase):
    def test_send_messages(self):
        """
        Отправление сообщений пользователю.
        Проверка запросов на сервер (передача телефона и сообщения).
        Установка статусов задания "START", "WORK", "END".
        """
        Client = apps.get_model('client', 'Client')
        for i in range(9):
            client = Client(phone=f'6596856{i}',
                            code='33',
                            tag='#машина',
                            utc='2')
            client.save()
        task = Task(startdatetime=timezone.now() - timedelta(minutes=1),
                    endtdatetime=timezone.now() + timedelta(minutes=1),
                    message='Тест',
                    filter='#машина',
                    status=Task.StatusTask.NONE)
        task.save()
        for i in range(5):
            client = Client(phone=f'6596856{i}',
                            code='33',
                            tag='#конь',
                            utc='2')
            client.save()
        task = Task(startdatetime=timezone.now() - timedelta(minutes=1),
                    endtdatetime=timezone.now() + timedelta(minutes=1),
                    message='Тест',
                    filter='#конь',
                    status=Task.StatusTask.NONE)
        task.save()
        check_tasks()
        task_count = Task.objects.filter(status=Task.StatusTask.START).count()
        self.assertTrue(task_count == 2)

        check_new_messages()
        task_count = Task.objects.filter(status=Task.StatusTask.START).count()
        self.assertTrue(task_count == 1)
        task_count = Task.objects.filter(status=Task.StatusTask.WORK).count()
        self.assertTrue(task_count == 1)
        message_count = Message.objects.filter(status=Message.StatusMessage.OK).count()
        self.assertTrue(message_count == 5)

        check_new_messages()
        task_count = Task.objects.filter(status=Task.StatusTask.WORK).count()
        self.assertTrue(task_count == 1)
        task_count = Task.objects.filter(status=Task.StatusTask.END).count()
        self.assertTrue(task_count == 1)
        message_count = Message.objects.filter(status=Message.StatusMessage.OK).count()
        self.assertTrue(message_count == 10)

        check_new_messages()
        task_count = Task.objects.filter(status=Task.StatusTask.WORK).count()
        self.assertTrue(task_count == 0)
        task_count = Task.objects.filter(status=Task.StatusTask.END).count()
        self.assertTrue(task_count == 2)
        message_count = Message.objects.filter(status=Message.StatusMessage.OK).count()
        self.assertTrue(message_count == 14)
