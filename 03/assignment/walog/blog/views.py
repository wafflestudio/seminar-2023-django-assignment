from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework import permissions

from .models import User, Post, Comment, Tag
from .serializers import PostSerializer, CommentSerializer, UserSerializer
from .forms import PostForm
from .permissions import IsOwnerOrReadOnly

from walog import settings
# Create your views here.
# 기초

def index(request):
    return render(request, "blog/index.html")


def TagCheck():
    tags = Tag.objects.all()
    for tag in tags:
        if tag.post_set.all():
            pass
        elif tag.comment_set.all():
            pass
        else:
            tag.delete()
# def post_create(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         form.instance.created_by = request.user
#         if form.is_valid():
#             if request.user.is_authenticated == False:
#                 return redirect('/login/')
#             post = form.save()
#             tags = request.POST['tags']
#             tags = tags.split(',')
#             for tag in tags:
#                 if not Tag.objects.filter(name=tag):
#                     Tag.objects.create(name=tag)
            
#             return reverse('post-detail', kwargs={'pk' : post.id})
#     form = PostForm()
#     return render(request, 'blog/post_form.html', {'form' : form})


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = settings.LOGIN_URL
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    def get_success_url(self):
        return redirect(resolve_url('post-detail', pk=self.object.id))
    
    def post(self, *args, **kwargs):
        post_form = PostForm(self.request.POST)
        if post_form.is_valid():
            cur_user = self.request.user
            if cur_user.is_authenticated:
                post_form.instance.created_by = self.request.user
            else:   
                return redirect('/login/')
            
            post = post_form.save()
            
            tags = self.request.POST['tags']
            tags = tags.split(',')
            for tag in tags:
                tag = tag.strip()
                if tag is None:
                    continue

                if Tag.objects.filter(name=tag):
                    _tag = Tag.objects.get(name=tag)
                    post.tags.add(_tag)
                else:                
                    _tag = Tag(name=tag)
                    _tag.save()
                    post.tags.add(_tag)

            post.save()
            return redirect(resolve_url('post-detail', pk=post.id))
        return redirect('/blog/index')

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = 'posts'
    ordering = ['created_at']
    paginate_by = 6
    page_kwarg = 'page'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)

        context['user'] = self.request.user
        post = Post.objects.get(pk=context['object'].id)
        context['owner'] = False

        if post.created_by == self.request.user or self.request.user.is_superuser:
            context['owner'] = True

        comment_list = Comment.objects.filter(post=post)
        comment = {}

        paginator = Paginator(comment_list, 5)
        curr_page_number = self.request.GET.get('page')
        if not curr_page_number:
            curr_page_number = 1
        page = paginator.page(curr_page_number)

        path = self.request.path
        path_list = path.split('/')
        path_list = ' '.join(path_list).split()
        edit_comment = -1
        if path_list[-2].isdigit():
            edit_comment = path_list[-1]
        edit_comment = int(edit_comment)

        context['page'] = page
        context['edit_comment'] = edit_comment
        return context

# 심화
#post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = settings.LOGIN_URL
    model = Post
    fields = ['title', 'description']
    template_name = 'blog/post_form_update.html'
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk' : self.object.id})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            post = Post.objects.get(pk=kwargs['pk'])
            post.title = request.POST['title']
            post.description = request.POST['description']
            post.save()
            return redirect(resolve_url('post-detail', pk=post.id))
        return redirect(resolve_url('post-list'))
    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = settings.LOGIN_URL
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'post'

    def get_success_url(self):
        TagCheck()
        return reverse('post-list')



#comment

def add_comment(request, pk):
    comment = Comment()
    comment.created_by = request.user
    comment.post = Post.objects.get(id=pk)
    comment.content = request.POST['text']
    comment.save()
    tags = request.POST['tags']
    tags = tags.split(',')
    for tag in tags:
        tag = tag.strip()
        if tag is None:
            continue

        if Tag.objects.filter(name=tag):
            _tag = Tag.objects.get(name=tag)
            comment.tags.add(_tag)
        else:                
            _tag = Tag(name=tag)
            _tag.save()
            comment.tags.add(_tag)

    comment.save()
    return redirect(resolve_url('post-detail', pk=pk))

def update_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.content = request.GET['text']
    comment.is_updated = True
    comment.save()
    
    post_id = comment.post.id
    return redirect('{}#comment_{}'.format(resolve_url('post-detail', pk=post_id), pk))

def delete_comment(request, pk):
    post_id = Comment.objects.get(id=pk).post.id
    Comment.objects.get(id=pk).delete()

    TagCheck()
    return redirect(resolve_url('post-detail', pk=post_id))

def edit_comment(request, pk):
    post_id = Comment.objects.get(id=pk).post.id
    return redirect('{}#comment_{}'.format(resolve_url('post-detail-editcomment', pk=post_id, editing_comment=pk), pk))





#REST framework - API 
class PostPageNumberPagination(PageNumberPagination):
    page_size = 5


class APIPostList(LoginRequiredMixin, ListCreateAPIView):
    login_url = settings.LOGIN_URL
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        return super().perform_create(serializer)


class APIPostDetail(LoginRequiredMixin, RetrieveUpdateDestroyAPIView):
    login_url = settings.LOGIN_URL
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        TagCheck()
        return response
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

    # def get_object(self, pk):
    #     post = get_object_or_404(Post, pk=pk)
    #     return post
    
    # def get(self, request, pk):
    #     post = self.get_object(pk)
    #     serializer = PostSerializer(post)
    #     return Response(serializer.data)

    # def patch(self, request, pk):
    #     post = self.get_object(pk)
    #     serializer = PostSerializer(post, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):
    #     post = self.get_object(pk)
    #     post.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class CommentPageNumberPagination(PageNumberPagination):
    page_size = 10

class APICommentList(LoginRequiredMixin, ListCreateAPIView):
    login_url = settings.LOGIN_URL
    serializer_class = CommentSerializer
    pagination_class = CommentPageNumberPagination
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        serializer.save(post=post, created_by=self.request.user)
        return super().perform_create(serializer)


# token authentication
class SignupView(APIView):
    serializer_class = UserSerializer
    def post(self, request):
        user_set = User.objects.filter(username=request.data['username'])
        if not user_set:
            user = User.objects.create_user(username=request.data['username'], password=request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({"Token" : token.key})
        else:
            return Response(status=401)

class LoginView(APIView):
    serializer_class = UserSerializer
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])

        if user is not None:
            token = Token.objects.get(user=user)
            return Response({"Token" : token.key})
        else:
            return Response(status=401)


class MyLoginView(LoginView):
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None:
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            return super().post(request)    

class MySignupView(SignupView):
    def post(self, request):
        user_set = User.objects.filter(username=request.data['username'])
        if not user_set and request.data['password'].strip() != "":
            user = User.objects.create_user(username=request.data['username'], password=request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(settings.ACCOUNT_SIGNUP_REDIRECT_URL)
        else:
            return Response(status=401)



#tags
def tag_search(request):
    if request.method == "POST":
        try:
            search_type = request.POST['type']
            search_tag = request.POST['tag_name']
        except (KeyError):
            return render(request, 'blog/tag_search.html')
        search_tag = search_tag.strip()
        if not search_tag:
            return render(request, 'blog/tag_search.html')

        if search_type == "posts":
            return redirect(resolve_url('post-tag-list', tag_name=search_tag))
        elif search_type == "comments":
            return redirect(resolve_url('comment-tag-list', tag_name=search_tag))
        else:
            # 발생해선 안되는 코드
            return render(request, 'blog/tag_search.html')
    else:
        return render(request, 'blog/tag_search.html')


def post_tag_list(request, tag_name):
    posts = Post.objects.filter(tags__name=tag_name)
    paginator = Paginator(posts, 6)
    curr_page_number = request.GET.get('page')
    if curr_page_number is None:
        curr_page_number = 1
    page = paginator.page(curr_page_number)
    return render(request, 'blog/post_tag_list.html', {'page' : page})


def comment_tag_list(request, tag_name):
    comments = Comment.objects.filter(tags__name=tag_name)
    paginator = Paginator(comments, 6)
    curr_page_number = request.GET.get('page')
    if curr_page_number is None:
        curr_page_number = 1
    page = paginator.page(curr_page_number)
    return render(request, 'blog/comment_tag_list.html', {'page' : page})
