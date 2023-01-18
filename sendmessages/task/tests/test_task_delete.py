from django.test import TestCase
from rest_framework.test import APIRequestFactory
from ..views import TaskDelete
from ..models import Task


class ApiTasksTest(TestCase):
    def test_task_delete(self):
        """
        Удаление задания в базе с помощью put запроса
        """
        task = Task(startdatetime="2023-01-12T21:25:00Z", endtdatetime="2023-01-11T21:25:00Z",
                  message="Мы в вас верим!", filter="#новаяжизнь",)
        task.save()
        factory: APIRequestFactory = APIRequestFactory()
        request = factory.delete('/tasks/delete/1/', {}, format='json')
        view = TaskDelete.as_view()
        response = view(request, id=1)
        self.assertEqual(response.status_code, 204)
