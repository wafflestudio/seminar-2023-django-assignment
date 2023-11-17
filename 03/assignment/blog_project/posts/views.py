from django.views.generic import RedirectView
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import CursorPagination
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

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
     authentication_classes = [TokenAuthentication]
     permission_classes = [IsAuthenticatedOrReadOnly]

     def perform_create(self, serializer):
         serializer.save(created_by=self.request.user)


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.created_by == request.user



class PostDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

class CommentListAPI(ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentCursorPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        serializer.save(post=post)
        serializer.save(created_by=self.request.user)
