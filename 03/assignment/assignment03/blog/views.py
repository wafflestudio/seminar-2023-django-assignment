from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404
from django.contrib.auth import authenticate, login, logout

from blog.models import Post, Comment, Tag 
import blog.serializers as serializers
from blog.permissions import IsOwnerAndAdminOrReadOnly, IsAuthenticatedOrReadOnly
from blog.pagenation import CursorPagination


class SignupView(generics.GenericAPIView):
    serializer_class = serializers.CreateUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            token = Token.objects.create(user=user)
            return Response({"user":serializers.UserSerializer(user).data, "Token": token.key})
        else:
            return Response({"message":"invalid name"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginUserSerializer

    def post(self, request):
        user = authenticate(username=request.data["username"], password=request.data['password'])
        if user is not None:
            login(request, user)
            token = Token.objects.get(user=user)
            return Response({"user":serializers.UserSerializer(user).data, "Token": token.key})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(generics.GenericAPIView):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PostListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = serializers.PostCreateSerializer
    pagination_class = CursorPagination
    def get_queryset(self):
        return Post.objects.all()

    def get(self, request):
        posts = self.paginate_queryset(self.get_queryset())
        serializer = serializers.PostSerializer(posts, many=True)
        for data in serializer.data:
            data["description"] = data["description"][:300]
        return self.get_paginated_response(serializer.data)
    
    def post(self, request):
        serializer = serializers.PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(generics.GenericAPIView):
    permission_classes = [IsOwnerAndAdminOrReadOnly, ]
    serializer_class = serializers.PostCreateSerializer
    def get_object(self, pk):
        post = get_object_or_404(Post, pk=pk)
        return post
    
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = serializers.PostSerializer(post)
        return Response(serializer.data)
    
    def patch(self, request, pk):
        post = self.get_object(pk)
        serializer = serializers.PostSerializer(instance=post, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(created_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        post = self.get_object(pk)
        tags = Tag.objects.filter(posts=post)
        post.delete()
        for tag in tags:
            if Post.objects.filter(tags=tag).count() + Comment.objects.filter(tags=tag).count() == 0:
                tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class PostCommentListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = serializers.CommentCreateSerializer
    pagination_class = CursorPagination
    def get_queryset(self):
        return Comment.objects.all()
    
    def get(self, request, pk):
        comments = self.paginate_queryset(self.get_queryset().filter(post__id=pk))
        serializer = serializers.CommentSerializer(comments, many=True)
        return self.get_paginated_response(serializer.data)
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = serializers.CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(post=post, created_by=request.user, is_updated=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = serializers.CommentCreateSerializer
    pagination_class = CursorPagination
    def get_queryset(self):
        return Comment.objects.all()
    
    def get(self, request):
        comments = self.paginate_queryset(self.get_queryset())
        serializer = serializers.CommentSerializer(comments, many=True)
        return self.get_paginated_response(serializer.data)
    

class CommentDetailView(generics.GenericAPIView):
    permission_classes = [IsOwnerAndAdminOrReadOnly, ]
    serializer_class = serializers.CommentCreateSerializer
    def get_object(self, pk):
        comment = get_object_or_404(Comment, pk=pk)
        return comment
    
    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = serializers.CommentSerializer(comment)
        return Response(serializer.data)
    
    def patch(self, request, pk):
        comment = self.get_object(pk)
        serializer = serializers.CommentSerializer(instance=comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(is_updated=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        comment = self.get_object(pk)
        tags = Tag.objects.filter(comments=comment)
        comment.delete()
        for tag in tags:
            if Post.objects.filter(tags=tag).count() + Comment.objects.filter(tags=tag).count() == 0:
                tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class TagPostListView(generics.GenericAPIView):
    serializer_class = serializers.PostSerializer
    pagination_class = CursorPagination
    def get_queryset(self):
        return Post.objects.all()
    
    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        posts = self.paginate_queryset(self.get_queryset().filter(tags=tag))
        serializer = serializers.PostSerializer(posts, many=True)
        for data in serializer.data:
            data["description"] = data["description"][:300]
        return self.get_paginated_response(serializer.data)
    

class TagCommentListView(generics.GenericAPIView):
    serializer_class = serializers.PostSerializer
    pagination_class = CursorPagination
    def get_queryset(self):
        return Comment.objects.all()
    
    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        posts = self.paginate_queryset(self.get_queryset().filter(tags=tag))
        serializer = serializers.CommentSerializer(posts, many=True)
        return self.get_paginated_response(serializer.data)

