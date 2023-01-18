from django.test import TestCase
from rest_framework.test import APIRequestFactory
from ..views import TaskUpdate
from ..models import Task


class ApiTasksTest(TestCase):
    def test_task_update(self):
        """
        Обновление задания в базе с помощью put запроса
        """
        task = Task(startdatetime="2023-01-12T21:25:00Z", endtdatetime="2023-01-11T21:25:00Z",
                    message="Мы в вас верим!", filter="#новаяжизнь",)
        task.save()
        factory: APIRequestFactory = APIRequestFactory()
        request = factory.put('/tasks/1/',
                              {"startdatetime": "2023-01-12T21:25:00Z", "endtdatetime": "2023-01-11T21:25:00Z",
                               "message": "Мы идем в ногу!", "filter": "#лучшаяжизнь", },
                              format='json')
        view = TaskUpdate.as_view()
        response = view(request, id=1)
        self.assertEqual(response.status_code, 200)
