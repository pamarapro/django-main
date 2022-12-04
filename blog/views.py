from django.shortcuts import render
from .models import Post
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

from rest_framework.response import Response
from rest_framework import generics
from .serializers import PostSerializer
from rest_framework.views import APIView
from django.http import Http404

class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)



class PostDetail(APIView):
    def get_object(self, post_slug):
        try:
            return Post.objects.get(slug=post_slug)
        except Post.DoesNotExist:
            raise Http404
    
    def get(self, request, post_slug, format=None):
        post = self.get_object(post_slug)
        serializer = PostSerializer(post)
        return Response(serializer.data)
