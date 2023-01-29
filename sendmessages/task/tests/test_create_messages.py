from django.test import TestCase
from ..models import Task, Message
from django.apps import apps
from django.utils import timezone
from datetime import timedelta
from ..tasks import check_tasks


class TasksTest(TestCase):
    def test_check_tasks(self):
        """
        Ищет новые задачи(создает сообщения на отправку) и закрывает просроченные
        """
        Client = apps.get_model('client', 'Client')
        client = Client(phone='+37565968569',
                        code='2',
                        tag='#машина',
                        utc='2')
        client.save()
        client = Client(phone='+37565968568',
                        code='2',
                        tag='#квартира',
                        utc='2')
        client.save()
        task = Task(startdatetime=timezone.now() - timedelta(minutes=1),
                    endtdatetime=timezone.now() + timedelta(minutes=1),
                    message='Тест',
                    filter='#машина')
        task.save()
        task = Task(startdatetime=timezone.now() - timedelta(minutes=2),
                    endtdatetime=timezone.now() - timedelta(minutes=1),
                    message='Тест',
                    filter='#машина',
                    status=Task.StatusTask.NONE)
        task.save()
        task = Task(startdatetime=timezone.now() - timedelta(minutes=2),
                    endtdatetime=timezone.now() - timedelta(minutes=1),
                    message='Тест',
                    filter='#машина',
                    status=Task.StatusTask.START)
        task.save()
        task = Task(startdatetime=timezone.now() - timedelta(minutes=2),
                    endtdatetime=timezone.now() - timedelta(minutes=1),
                    message='Тест',
                    filter='#машина',
                    status=Task.StatusTask.WORK)
        task.save()

        self.assertTrue(True)

        check_tasks()
        count_messages = Message.objects.count()
        self.assertTrue(count_messages == 1)
        count_start_tasks = Task.objects.filter(status=Task.StatusTask.START).count()
        self.assertTrue(count_start_tasks == 1)
        count_stop_tasks = Task.objects.filter(status=Task.StatusTask.END).count()
        self.assertTrue(count_stop_tasks == 3)
