from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import generics
from .serializers import PolicySerializer
from rest_framework.views import APIView
from django.http import Http404

from .models import Policy

class PolicyPageLists(generics.ListAPIView):
    queryset = Policy.objects.all()
    def get(self, request, format=None):
        policies = Policy.objects.all()
        serializer = PolicySerializer(policies, many=True)
        return Response(serializer.data)


class PolicyDetail(generics.ListAPIView):
    class Meta:
        model = Policy
        fields = ("title", 'description')
    
    def get_object(self, policy_slug):
        try:
            return Policy.objects.get(slug=policy_slug)
        except Policy.DoesNotExist:
            raise Http404
    
    def get(self, request, policy_slug, format=None):
        policy = self.get_object(policy_slug)
        serializer = PolicySerializer(policy)
        return Response(serializer.data)