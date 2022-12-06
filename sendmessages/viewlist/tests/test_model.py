from django.test import TestCase
from ..models import TaskList


class ModelTest(TestCase):
    def test_model_create(self):
        """
        Создание записи в таблице TaskList
        """
        count_before = TaskList.objects.count()
        TaskList.objects.create(name="1", text_message="1", status="1", status_text="1")
        count_after = TaskList.objects.count()
        count_delta = count_after - count_before
        self.assertEqual(count_delta, 1)
