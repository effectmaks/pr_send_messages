from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .models import Client
from .serializers import ClientSerializer
from rest_framework.response import Response
from rest_framework import status

from rest_framework.generics import UpdateAPIView


class ClientList(APIView):
    def get(self, request):
        client = Client.objects.all()
        serializer = ClientSerializer(client, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():  # проверяет по модели, не больше длины максимума, может быть поле пустым
            serializer.save()  # сохраняет новую запись в моделе
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ClientUpdate(UpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'id'
