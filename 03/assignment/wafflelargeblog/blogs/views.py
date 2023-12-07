from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment, User, Tag
from .serializers import PostSerializer, CommentSerializer, UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import permissions

def TagEnd():
    tags = Tag.objects.all()
    for tag in tags:
        if tag.post.all():
            pass
        elif tag.comment.all():
            pass
        else:
            tag.delete()

class OwnProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user or request.user.is_superuser

from rest_framework.pagination import CursorPagination
from .pagination import PaginationHandlerMixin

class PostPageNumberPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'

class CommentPageNumberPagination(CursorPagination):
    page_size = 20
    ordering = '-created_at'

# Create your views here.
from django.views import View
class IndexView(View):
    def get(self, request):
        return render(request, 'blogs/index.html')

class PostList(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PostPageNumberPagination
    serializer_class = PostSerializer
    def get(self, request):
        instance = Post.objects.all()        
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)
        
        for data in serializer.data['results']:
            data['description'] = data['description'][:300]

        return Response(serializer.data, status=status.HTTP_200_OK)
       
        
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            post = serializer.save(created_by = request.user)
            if 'tag' in request.data:
                for tag_data in request.data['tag']:
                    content = tag_data['content']
                    try : 
                        tag = Tag.objects.get(pk=content)

                    except:
                        tag = Tag.objects.create(content=content)
                        tag.save()
                    post.tag.add(tag)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, OwnProfilePermission]

    def get_object(self, pk):
        post = get_object_or_404(Post, pk=pk)
        return post
    
    def get(self, request, pk):
        instance = self.get_object(pk)
        serializer = PostSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    def patch(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        TagEnd()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentList(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CommentPageNumberPagination
    serializer_class = CommentSerializer

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        instance = Comment.objects.filter(post=post)
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = CommentSerializer(data=request.data )
        if serializer.is_valid():
            serializer.save(created_by = request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class CommentDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, OwnProfilePermission]

    def get_object(self, pk):
        comment = get_object_or_404(Comment, pk=pk)
        return comment
    
    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(is_updated = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = self.get_object(pk)            
        comment.delete()
        TagEnd()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TagPostList(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PostPageNumberPagination
    serializer_class = PostSerializer

    def get(self, request, tc):
        instance = Post.objects.filter(tag__content=tc)
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class TagCommentList(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CommentPageNumberPagination
    serializer_class = CommentSerializer
    def get(self, request, tc):
        instance = Comment.objects.filter(tag__content=tc)
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        