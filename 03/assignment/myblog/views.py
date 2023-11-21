from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    CreateView, ListView, DetailView, UpdateView, DeleteView, RedirectView
)
from django.urls import reverse
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth import authenticate
from .serializers import PostSerializer, CommentSerializer, UserSerializer
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.pagination import CursorPagination
from django.contrib.auth import authenticate, login
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

# Create your views here.

class PostCommentCursorPagination(CursorPagination):
    page_size = 10  # 한 페이지에 표시할 아이템 수
    ordering = '-dt_created'  # 내림차순 정렬

User = get_user_model()
class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")

        # username 입력 확인
        if not username:
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class PostList(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PostCommentCursorPagination
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return []

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostListByTag(ListAPIView):

    pagination_class = PostCommentCursorPagination
    serializer_class = PostSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        return Post.objects.filter(tag__name=tag_name)

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 요청에 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # 쓰기 권한은 포스트의 작성자에게만 허용
        return obj.author == request.user
    
class PostDetail(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    

class CommentList(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PostCommentCursorPagination
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return []
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        if post_id is not None:
            return Comment.objects.filter(post__id=post_id)
        return Comment.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
class CommentListByTag(ListAPIView):

    serializer_class = CommentSerializer
    pagination_class = PostCommentCursorPagination
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        return Comment.objects.filter(tag__name=tag_name)
    
class CommentUpdateDelete(UpdateAPIView, DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


    
# class PostDetailView(DetailView):
#     model = Post
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.get_object()
#         comments = Comment.objects.filter(post=post).order_by('-dt_created')
#         context['comments'] = comments
#         context['comment_form'] = CommentForm()
#         return context

#     def post(self, request, *args, **kwargs):
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             post = self.get_object()
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.post = post
#             comment.save()
#             return redirect(post.get_absolute_url())
#         return self.get(request, *args, **kwargs)

# class PostCreateView(CreateView):
#     model = Post
#     form_class = PostForm


#     def get_success_url(self):
#         return reverse('post-detail', kwargs={'pk': self.object.id})
    
#     def post(self, request, *args, **kwargs):
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect(post.get_absolute_url())
#         return self.get(request, *args, **kwargs)

# class PostUpdateView(UpdateView):
#     model = Post
#     form_class = PostForm

#     def get_success_url(self):
#         return reverse('post-detail', kwargs={'pk': self.object.id})

# class PostDeleteView(DeleteView):
#     model = Post

#     def get_success_url(self):
#         return reverse('post-list')

# class IndexRedirectView(RedirectView):
#     pattern_name = 'post-list'
