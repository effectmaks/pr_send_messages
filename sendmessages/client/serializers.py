from .models import Client
from rest_framework.serializers import HyperlinkedModelSerializer


class ClientSerializer(HyperlinkedModelSerializer):
   class Meta:
       model = Client
       fields = ['id', 'phone', 'code', 'tag', 'utc', ]
