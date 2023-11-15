from typing import Any
from django import http
from django.db import models
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.models import EmailAddress

from .forms import PostForm, CommentForm
from .models import Post, Comment, User

# Create your views here.

class MainView(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'blog/main_list.html'

    ordering = ['-dt_created']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    pk_url_kwarg = "post_id"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    redirect_unauthenticated_users = True
    raise_exception = True

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={"post_id": self.object.id})
    
    def test_func(self, user):
        return EmailAddress.objects.filter(user=user, verified=True).exists()


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name="blog/post_form.html"
    pk_url_kwarg = "post_id"

    success_url = reverse_lazy('main')

    redirect_unauthenticated_users = True
    raise_exception = True

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def dispatch(self, request, *args: Any, **kwargs):
        if self.get_object().author != self.request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={"post_id": self.object.id})
    
    def test_func(self, user):
        post = self.get_object()
        return post.author == user

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    pk_url_kwarg = "post_id"

    success_url = reverse_lazy('main')

    redirect_unauthenticated_users = True
    raise_exception = True
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def dispatch(self, request, *args: Any, **kwargs):
        if self.get_object().author != self.request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('main')
    
    def test_func(self, user):
        post = self.get_object()
        return post.author == user

class CommentCreateView(LoginRequiredMixin, CreateView):
    http_method_names = ['post']
    model = Comment
    form_class = CommentForm

    redirect_unauthenticated_users = True
    raise_exception = True
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(id=self.kwargs.get('post_id'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'post_id': self.kwargs.get('post_id')})

    def test_func(self, user):
        return EmailAddress.objects.filter(user=user, verified=True).exists()
