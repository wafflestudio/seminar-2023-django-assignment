from django.views.generic import RedirectView
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import CursorPagination

from .models import User, Post, Comment
from .serializers import UserSerializer, PostListSerializer, PostDetailSerializer, CommentSerializer

class IndexRedirectView(RedirectView):
    pattern_name = 'post-list'
class PostCursorPagination(CursorPagination):
    page_size = 5
    ordering = '-created_at'


class CommentCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'

class PostListAPI(ListCreateAPIView):
     queryset = Post.objects.all()
     serializer_class = PostListSerializer
     pagination_class = PostCursorPagination

class PostDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

class CommentListAPI(ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentCursorPagination

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        serializer.save(post=post)

