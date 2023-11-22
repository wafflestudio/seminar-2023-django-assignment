
from django.shortcuts import render, get_object_or_404

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .models import Post, Comment, Tag
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly


# Create your views here.
class PostListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAdminUser | IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all().order_by('-dt_created')
    serializer_class = PostListSerializer

    def perform_create(self, serializer):
        author = self.request.user
        tag_name_list = serializer.validated_data.pop('tag_list', None).split(',')
        new_post = serializer.save(author=author)

        for tag_name in tag_name_list:
            tag_object, created = Tag.objects.get_or_create(content=tag_name)
            tag_object.posts.add(new_post)


class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [ IsAdminUser | IsOwnerOrReadOnly ]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

    def perform_destroy(self, instance):
        tag_name_list = [tag.content for tag in instance.tags.all()]
        super().perform_destroy(instance)

        for tag_name in tag_name_list:
            tag = Tag.objects.get(pk=tag_name)
            if (not tag.comments.exists()) and (not tag.posts.exists()):
                tag.delete()


class CommentListCreateAPIView(ListCreateAPIView):
    permission_classes = [ IsAdminUser | IsAuthenticatedOrReadOnly ]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return Comment.objects.filter(post=post).order_by('dt_created')

    def perform_create(self, serializer):
        author = self.request.user
        post_id = self.kwargs.get('pk')
        tag_name_list = serializer.validated_data.pop('tag_list').split(',')
        new_comment = serializer.save(author=author, post_id=post_id)

        for tag_name in tag_name_list:
            tag_object, created = Tag.objects.get_or_create(pk=tag_name)
            tag_object.comments.add(new_comment)


class CommentUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [ IsAdminUser | IsOwnerOrReadOnly ]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_update(self, serializer):
        serializer.save(is_updated=True)

    def perform_destroy(self, instance):
        tag_list = instance.tags.all()
        super().perform_destroy(instance)

        for tag in tag_list:
            if (not tag.posts.exists()) and (not tag.comments.exists()):
                tag.delete()


class TagPostListView(ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return tag.posts.all()


class TagCommentListView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return tag.comments.all()
