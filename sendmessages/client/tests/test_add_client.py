from django.test import TestCase
from rest_framework.test import APIRequestFactory
from ..views import ClientList


class ApiClientsTest(TestCase):
    def test_add_clients(self):
        """
        Добавление клиента в базу с помощью put запроса
        """
        factory: APIRequestFactory = APIRequestFactory()
        request = factory.post('/clients/', {"phone": "+375333882903", "code": "852852", "tag": "#машина", "utc": 1},
                               format='json')
        view = ClientList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
