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
    queryset = Post.objects.all()
    model = Post
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated|permissions.IsAdminUser]

    lookup_field = 'id'
    lookup_url_kwarg = 'post_id'

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, **{self.lookup_field: self.kwargs[self.lookup_url_kwarg]})
        
        # Check if the author of the post is the same as the current user
        if self.request.user.is_staff:
            return obj
        if obj.author != self.request.user:
            self.permission_denied(
                self.request,
                message="You do not have permission to perform this action."
            )
        return obj
    
class PostUpdateView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    model = Post
    serializer_class = PostUpdateSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]

    lookup_field = 'id'
    lookup_url_kwarg = 'post_id'

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, **{self.lookup_field: self.kwargs[self.lookup_url_kwarg]})
        
        # Check if the author of the post is the same as the current user
        if self.request.user.is_staff:
            return obj
        if obj.author != self.request.user:
            self.permission_denied(
                self.request,
                message="You do not have permission to perform this action."
            )
        return obj
    
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
        post = get_object_or_404(Post, pk=post_id)
        return Comment.objects.filter(post=post)

class CommentDeleteView(RetrieveDestroyAPIView):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated|permissions.IsAdminUser]
    
    lookup_field = 'id'
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self):
        post_id=self.kwargs.get('post_id')
        comment_id=self.kwargs.get('comment_id')
        return Comment.objects.filter(post_id=post_id, id=comment_id)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, **{self.lookup_field: self.kwargs[self.lookup_url_kwarg]})
        
        if self.request.user.is_staff:
            return obj

        # Check if the author of the comment is the same as the current user
        if obj.author != self.request.user:
            self.permission_denied(
                self.request,
                message="You do not have permission to perform this action."
            )
        return obj

class CommentUpdateView(RetrieveUpdateAPIView):
    model = Comment
    serializer_class = CommentUpdateSerializer
    permission_classes = [permissions.IsAuthenticated|permissions.IsAdminUser]
    
    lookup_field = 'id'
    lookup_url_kwarg = 'comment_id'
    
    def get_queryset(self):
        post_id=self.kwargs.get('post_id')
        comment_id=self.kwargs.get('comment_id')
        return Comment.objects.filter(post_id=post_id, id=comment_id)
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, **{self.lookup_field: self.kwargs[self.lookup_url_kwarg]})
        
        if self.request.user.is_staff:
            return obj

        # Check if the author of the comment is the same as the current user
        if obj.author != self.request.user:
            self.permission_denied(
                self.request,
                message="You do not have permission to perform this action."
            )
        return obj

# tag
class TagListPostView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostPageNumberPagination

    def get_queryset(self):        
        tag_content = self.kwargs.get('tag_content')
        try:
            tag = Tag.objects.get(content=tag_content)
        except Tag.DoesNotExist:
            raise Http404("Tag not found")
        return Post.objects.filter(tags__content__iexact=tag_content)
        


class TagListCommentView(ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentPageNumberPagination

    def get_queryset(self):
        tag_content = self.kwargs.get('tag_content')
        try:
            tag = Tag.objects.get(content=tag_content)
        except Tag.DoesNotExist:
            raise Http404("Tag not found")
        return Comment.objects.filter(tags__content__iexact=tag_content)
    