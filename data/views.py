from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import generics
from .serializers import DataSerializer
from rest_framework.views import APIView
from django.http import Http404

from .models import Data

# Create your views here.


class DataLists(generics.ListAPIView):
    queryset = Data.objects.all()
    def get(self, request, format=None):
        datas = Data.objects.all()
        serializer = DataSerializer(datas, many=True)
        return Response(serializer.data)

