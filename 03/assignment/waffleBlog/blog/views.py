from rest_framework import generics, permissions
from .models import Post, Comment, Tag
from .serializers import PostListSerializer, PostCreateSerializer, PostDetailSerializer, CommentSerializer, TagSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostListSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.AllowAny, IsOwnerOrReadOnly]


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # 게시물 ID가 제공되면 해당 게시물에 대한 댓글만 반환, 그렇지 않으면 모든 댓글 반환
        post_id = self.kwargs.get('post_id')
        if post_id:
            post = get_object_or_404(Post, pk=post_id)
            return Comment.objects.filter(post=post)
        return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]


class TagListCreateView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TaggedPostListAPIView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        content = self.kwargs['content']
        tag = Tag.objects.get(content=content)
        return tag.posts.all()


class TaggedCommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        content = self.kwargs['content']
        tag = Tag.objects.get(content=content)
        return tag.comments.all()

