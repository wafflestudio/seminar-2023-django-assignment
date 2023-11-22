from rest_framework.generics import get_object_or_404
from rest_framework import generics

from .models import Post, Comment, Tag
from .serializers import PostSerializer, CommentSerializer, TagSerializer
from .permissions import IsOwnerOrReadOnly
from .paginations import CursorPagination
from .tag_manage import postCreateNewTag, postUpdateTag, commentCreateNewTag, commentUpdateTag, DeleteTag


class PostListCreateAPI(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = CursorPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        try:
            tag_text = serializer.validated_data['tags']
        except KeyError:
            tag_text = ''
        new_post = serializer.instance
        postCreateNewTag(tag_text, new_post)


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_update(self, serializer):
        serializer.save()
        try:
            tag_text = serializer.validated_data['tags']
        except KeyError:
            tag_text = ''
        updated_post = serializer.instance
        postUpdateTag(tag_text, updated_post)

    def perform_destroy(self, instance):
        instance.delete()
        DeleteTag()


class CommentListCreateAPI(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        serializer.save(post=post, created_by=self.request.user)
        try:
            tag_text = serializer.validated_data['tags']
        except KeyError:
            tag_text = ''
        new_comment = serializer.instance
        commentCreateNewTag(tag_text, new_comment)


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_update(self, serializer):
        serializer.save()
        try:
            tag_text = serializer.validated_data['tags']
        except KeyError:
            tag_text = ''
        updated_comment = serializer.instance
        commentUpdateTag(tag_text, updated_comment)

    def perform_destroy(self, instance):
        instance.delete()
        DeleteTag()


class TagListByPostAPI(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        tag = get_object_or_404(Tag, content=self.kwargs.get('content'))
        return Post.objects.filter(tags__content=tag.content)


class TagListByCommentAPI(generics.ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        tag = get_object_or_404(Tag, content=self.kwargs.get('content'))
        return Comment.objects.filter(tags__content=tag.content)

