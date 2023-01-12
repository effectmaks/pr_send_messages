from django.test import TestCase
from rest_framework.test import APIRequestFactory
from ..views import TaskCreate


class ApiTasksTest(TestCase):
    def test_add_task(self):
        """
        Добавление задания на рассылку в базу с помощью put запроса
        """
        factory: APIRequestFactory = APIRequestFactory()
        request = factory.post('/tasks/', {"startdatetime": "2023-01-11T19:05:00Z",
                                           "endtdatetime": "2023-01-26T19:05:00Z",
                                           "message": "Miru mir",
                                           "filter": "#машина"},
                               format='json')
        view = TaskCreate.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
