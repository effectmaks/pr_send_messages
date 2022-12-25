from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView
from .models import Client
from .serializers import ClientSerializer


class ClientsViewSet(CreateModelMixin, GenericAPIView):
   queryset = Client.objects.all()
   serializer_class = ClientSerializer

   @classmethod
   def get_extra_actions(cls):
       return []

   def get(self, request):
       return self.get(request)

   def post(self, request, format=None):
       return self.post(request)
