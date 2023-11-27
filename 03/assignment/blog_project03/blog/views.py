from .models import Post, Comment, User, Tag
from .serializers import (PostSerializer, 
                          CommentSerializer, 
                          UserSerializer,
                          PostCreateSerializer,
                          PostUpdateSerializer,
                          CommentCreateSerializer,
                          CommentUpdateSerializer,
                          TagSerializer
                          )
from rest_framework.generics import (
                                    ListAPIView,
                                    CreateAPIView,
                                    RetrieveAPIView,
                                    ListCreateAPIView,
                                    RetrieveUpdateAPIView,
                                    RetrieveDestroyAPIView,
                                    )
from rest_framework.pagination import CursorPagination
from rest_framework import permissions
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# Create your views here.

class PostPageNumberPagination(CursorPagination):
    page_size = 3
    ordering = '-dt_created'

class CommentPageNumberPagination(CursorPagination):
    page_size = 5
    ordering = '-dt_created'

class TagPageNumberPagination(CursorPagination):
    page_size = 1

# post
class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPageNumberPagination


class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    lookup_field = 'id'
    lookup_url_kwarg = 'post_id'

    def get_queryset(self):
        queryset = Post.objects.all()
        return queryset

class PostCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated|permissions.IsAdminUser]
    
    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user        
        instance = serializer.save()

        return instance

class PostDeleteView(RetrieveDestroyAPIView):
    model = Post
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated|permissions.IsAdminUser]

    lookup_field = 'id'
    lookup_url_kwarg = 'post_id'

    def get_queryset(self):
        if(self.request.user.is_staff):
            return Post.objects.all()
        return Post.objects.filter(author=self.request.user)

# Comment    
class CommentCreateView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated|permissions.IsAdminUser]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id=self.kwargs.get('post_id')
        post_instance = get_object_or_404(Post, pk=post_id)
        serializer.validated_data['post'] = post_instance
        
        serializer.validated_data['author'] = self.request.user
        instance = serializer.save()

        return instance    

class CommentListView(ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentPageNumberPagination

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

class CommentDeleteView(RetrieveDestroyAPIView):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated|permissions.IsAdminUser]
    
    lookup_field = 'id'
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self):
        if(self.request.user.is_staff):
            return Comment.objects.all()
        post_id=self.kwargs.get('post_id')
        comment_id=self.kwargs.get('comment_id')
        return Comment.objects.filter(post_id=post_id, id=comment_id, author=self.request.user)

# tag
class TagListPostView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostPageNumberPagination

    def get_queryset(self):        
        tag_content = self.kwargs.get('tag_content')
        try:
            tag = Tag.objects.get(content=tag_content)
            return Post.objects.filter(tags=tag)
        except Tag.DoesNotExist:
            raise Http404("Tag not found")


class TagListCommentView(ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentPageNumberPagination

    def get_queryset(self):
        tag_content = self.kwargs.get('tag_content')
        try:
            tag = Tag.objects.get(content=tag_content)
            return Comment.objects.filter(tags=tag)
        except Tag.DoesNotExist:
            raise Http404("Tag not found")






class PostUpdateView(RetrieveUpdateAPIView):
    model = Post
    serializer_class = PostUpdateSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]

    lookup_field = 'id'
    lookup_url_kwarg = 'post_id'

    def get_queryset(self):
        if(self.request.user.is_staff):
            return Post.objects.all()
        return Post.objects.filter(author=self.request.user)

    
class CommentUpdateView(RetrieveUpdateAPIView):
    model = Comment
    serializer_class = CommentUpdateSerializer
    permission_classes = [permissions.IsAuthenticated|permissions.IsAdminUser]
    
    lookup_field = 'id'
    lookup_url_kwarg = 'comment_id'
    
    def get_queryset(self):
        if(self.request.user.is_staff):
            return Comment.objects.all()
        post_id=self.kwargs.get('post_id')
        comment_id=self.kwargs.get('comment_id')
        return Comment.objects.filter(post_id=post_id, id=comment_id, author=self.request.user)
