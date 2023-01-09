from django.test import TestCase
from rest_framework.test import APIRequestFactory
from ..views import ClientDelete
from ..models import Client


class ApiClientsTest(TestCase):
    def test_client_delete(self):
        """
        Обновление клиента в базе с помощью put запроса
        """
        cd = Client(phone="+375338430526", code="247210", tag="#машина", utc=1,)
        cd.save()
        factory: APIRequestFactory = APIRequestFactory()
        request = factory.delete('/clients/delete/1/', {}, format='json')
        view = ClientDelete.as_view()
        response = view(request, id=1)
        self.assertEqual(response.status_code, 204)
