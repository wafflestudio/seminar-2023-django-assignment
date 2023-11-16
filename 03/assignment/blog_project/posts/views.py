from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.pagination import CursorPagination

from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer

class PostCursorPagination(CursorPagination):
    page_size = 5
    ordering = '-created_at'


class CommentCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'

class PostList(ListCreateAPIView):
     queryset = Post.objects.all()
     serializer_class = PostSerializer
     pagination_class = PostCursorPagination

class PostDetail(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentList(ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentCursorPagination

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        serializer.save(post=post)

