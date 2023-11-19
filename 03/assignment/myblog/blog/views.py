from django.shortcuts import render, redirect
from django.urls import reverse
from allauth.account.views import PasswordChangeView
from rest_framework.pagination import CursorPagination
from rest_framework.views import APIView
from django.core.serializers import serialize
from .forms import PageForm, CommentForm
from .models import Post, Comment, Tag, User, Profile
from .serializers import PostSerializer, CommentSerializer, TagSerializer
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404, ListCreateAPIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

# Create your views here.
def index(request):
    return render(request, "blog/index.html")

class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse("index")

class SignupView(APIView):
    def post(self, request):
        user = User.objects.create_user(username=request.data['id'], password=request.data['password'])
        profile = Profile(user=user)
        user.save()
        profile.save()
        token = Token.objects.create(user=user)
        return Response({"Token": token.key})

class LoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['id'], password=request.data['password'])
        if user is not None:
            token = Token.objects.get(user=user)
            return Response({"Token": token.key})
        else:
            return Response(status=401)

def page_create(request):
    if request.method == 'POST':
        new_page = Post(
            title=request.POST['title'],
            content=request.POST['content'],
            #author=request.POST['author'],
            author=request.user.username,
            dt_created=timezone.now(),
            dt_updated=timezone.now(),
        )

        new_page.save()
        tags = Tag(
            content=request.POST['tags_input'],
        )
        tags.save()
        new_page.tags.add(tags)
        new_page.save()

        return redirect('page-detail', page_id=new_page.id)
    else:
        form = PageForm()
        return render(request, 'blog/page_form.html', {'form':form})

@api_view(['GET', 'PATCH', 'DELETE'])
def page_detail(request, page_id):
    #object = Post.objects.get(id=page_id)
    #return render(request, 'blog/page_detail.html', {'object': object})
    object = get_object_or_404(Post, id=page_id)
    if request.method == 'GET':
        serializer = PostSerializer(object)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method =='PATCH':
        serializer = PostSerializer(object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)
    elif request.method =='DELETE':
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def page_list(request):
    #object_list = Post.objects.all()  # 데이터 조회
    #return render(request, 'blog/page_list.html', {'object_list': object_list})
    if request.method =='GET':
        object = Post.objects.all()
        serializer = PostSerializer(object, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = request.data
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def main_page(request):
    return render(request, 'blog_base/base.html')

def page_update(request, page_id):
    object = Post.objects.get(id=page_id)
    if request.method == 'POST':
        form = PageForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect('page-detail', page_id=object.id)
    else:
        form = PageForm(instance=object)
    return render(request, 'blog/page_form.html', {'form': form})


def page_delete(request, page_id):
    object = Post.objects.get(id=page_id)
    if request.method == 'POST':
        object.delete()
        return redirect('page-list')
    else:
        return render(request, 'blog/page_confirm_delete.html', {'object': object})

@api_view(['GET', 'POST'])
def comment_list(request, page_id):
    object = get_object_or_404(Post, id=page_id)
    if request.method == 'GET':
        comments = Comment.objects.filter(post=object)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=object)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def comments_create(request, page_id):
    if request.method == 'POST':
        comments = Comment.objects.all()
        curpost = Post.objects.get(id=page_id)
        new_comment = Comment(
            post = curpost,
            #author=request.POST['author'],
            author = request.user.username,
            content=request.POST['content'],
            created_at=timezone.now,
            updated_at=timezone.now,
        )
        new_comment.save()
        tags = Tag(
            content=request.POST['tags_input'],
        )
        tags.save()
        new_comment.tags.add(tags)
        new_comment.save()
        #return redirect('page-detail', page_id=curpost.id)
        return render(request, 'blog/page_detail.html', {'object':curpost, 'comments':comments})
    else:
        form = CommentForm()
        return render(request, 'blog/page_form.html', {'form': form})

def comments_delete(request, page_id, comment_id):
    if request.user.is_authenticated:
        comment = Comment.objects.get(id=comment_id)
        #if request.user == comment.author:
        comment.delete()
    return redirect('page-detail', page_id)

class PostPagination(CursorPagination):
    page_size = 10
    ordering = '-dt_created'

class PostList(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination
    # def get(self, request):
    #     posts = Post.objects.all()
    #     serializer = PostSerializer(posts, many=True)
    #     return Response(serializer.data)
    # def post(self, request):
    #     serializer = PostSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):

    def get_object(self, page_id):
        post = get_object_or_404(Post, id=page_id)
        return post

    def get(self, request, page_id):
        post = self.get_object(page_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def patch(self, request, page_id):
        post = self.get_object(page_id)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, page_id):
        post = self.get_object(page_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'

class CommentList(ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('page_id'))
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('page_id'))
        serializer.save(post=post)


@api_view(['GET', 'POST'])
def comment_tag_list(request, tag_name):
    object = get_object_or_404(Tag, content=tag_name)
    if request.method == 'GET':
        comments = Comment.objects.filter(tags__in=[object])
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=object)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def post_tag_list(request, tag_name):
    object = get_object_or_404(Tag, content=tag_name)
    if request.method == 'GET':
        posts = Post.objects.filter(tags__in=[object])
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=object)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)