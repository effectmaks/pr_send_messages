from django.test import TestCase
from rest_framework.test import APIRequestFactory
from ..views import ClientList, ClientUpdate
from ..models import Client


class ApiClientsTest(TestCase):
    def test_client_update(self):
        """
        Обновление клиента в базе с помощью put запроса
        """
        cd = Client(phone="+375338430526", code="247210", tag="#машина", utc=1,)
        cd.save()
        factory: APIRequestFactory = APIRequestFactory()
        request = factory.put('/clients/1/',
                               {"phone": "+375295326541", "code": "545247", "tag": "#огонь", "utc": 2, },
                               format='json')
        view = ClientUpdate.as_view()
        response = view(request, id=1)
        self.assertEqual(response.status_code, 200)
