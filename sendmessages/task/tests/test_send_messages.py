from django.test import TestCase
from ..models import Task, Message
from ..tasks import check_new_messages, check_tasks
from django.apps import apps
from django.utils import timezone
from datetime import timedelta


class TasksTest(TestCase):
    def test_send_messages(self):
        """
        Отправление сообщений пользователю
        """
        Client = apps.get_model('client', 'Client')
        client = Client(phone='65968569',
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
        check_tasks()
        check_new_messages()
        task_count = Task.objects.filter(status=Task.StatusTask.END).count()
        message_count = Message.objects.filter(status=Message.StatusMessage.OK).count()
        self.assertTrue(task_count == 1)
        self.assertTrue(message_count == 1)
