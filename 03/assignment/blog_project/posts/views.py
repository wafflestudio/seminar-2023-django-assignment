from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.views.generic import RedirectView
from requests import delete
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.pagination import CursorPagination
from rest_framework import permissions, generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from .models import User, Post, Comment, Tag
from .serializers import UserSerializer, PostListSerializer, PostDetailSerializer, CommentSerializer, \
    PostCreateSerializer, CommentListSerializer


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
     pagination_class = PostCursorPagination
     authentication_classes = [SessionAuthentication, TokenAuthentication]
     permission_classes = [IsAuthenticatedOrReadOnly]

     def get_serializer_class(self):
         if self.request.method == 'POST':
             return PostCreateSerializer
         return PostListSerializer

     def perform_create(self, serializer):
         serializer.save(created_by=self.request.user)

     def get(self, request, *args, **kwargs):
         queryset = self.filter_queryset(self.get_queryset())
         page = self.paginate_queryset(queryset)

         if page is not None:
             serializer = self.get_serializer(page, many=True)
             return self.get_paginated_response(serializer.data)

         serializer = self.get_serializer(queryset, many=True)
         return Response(serializer.data)



class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff or request.user.is_superuser:
            return True

        return obj.created_by == request.user

    # def has_object_permission(self, request, view, obj):
    #     if request.user:
    #         if obj.id == request.user.id:
    #             return True
    #         raise PermissionDenied()
    #     raise NotAuthenticated()



class PostDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # def perform_destroy(self, instance):
    #     print("perform_destroy")
    #     tags = instance.tags.all()
    #     super().perform_destroy(instance)
    #     for tag in tags:
    #         print("Checking tag:", tag)
    #         if tag.can_delete():
    #             print("Deleted tag:", tag)
    #             tag.delete()


class CommentListAPI(ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentCursorPagination
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        serializer.save(post=post, created_by=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True

        return obj.created_by == request.user


class CommentDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwner]
    lookup_url_kwarg = 'comment_id'

    def perform_update(self, serializer):
        serializer.save(is_updated=True)

    # def perform_destroy(self, instance):
    #     tags = instance.comment_tags.all()
    #     super().perform_destroy(instance)
    #     for tag in tags:
    #         if tag.can_delete():
    #             tag.delete()



class IsNew(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == AnonymousUser or request.user.is_staff or request.user.is_superuser:
            return True

        return False


class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsNew]


class LoginView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # 사용자 인증
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                token = Token.objects.get(user=user)
                return Response({"Token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListByTagAPI(generics.ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        tag = get_object_or_404(Tag, content=self.kwargs['tags_content'])
        return Post.objects.filter(tags=tag)

class CommentListByTagAPI(generics.ListAPIView):
    serializer_class = CommentListSerializer

    def get_queryset(self):
        tag = get_object_or_404(Tag, content=self.kwargs['comment_tags_content'])
        return Comment.objects.filter(comment_tags=tag)


# @receiver(post_delete, sender=Post)
# def post_deleted(sender, instance, **kwargs):
#     # Check and delete unused tags
#     for tag in instance.tags.all():
#         print("Checking tag:", tag)
#         if tag.can_delete():
#             print("Deleted tag:", tag)
#             tag.delete()
#
#
# @receiver(post_delete, sender=Comment)
# def comment_deleted(sender, instance, **kwargs):
#     # Check and delete unused tags
#     for tag in instance.comment_tags.all():
#         if tag.can_delete():
#             tag.delete()
