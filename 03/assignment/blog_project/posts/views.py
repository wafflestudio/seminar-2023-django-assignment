from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer

class PostPageNumberPagination(PageNumberPagination):
    page_size = 10
class PostList(ListCreateAPIView):
     queryset = Post.objects.all()
     serializer_class = PostSerializer
     pagination_class = PostPageNumberPagination

class PostDetail(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentList(ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        serializer.save(post=post)

