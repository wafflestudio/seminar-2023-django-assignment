from braces.views import LoginRequiredMixin

from django.shortcuts import render, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Post, Comment, TagPost, TagComment
from .forms import PostForm


class IndexView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'
    paginate_by = 8


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    pk_url_kwarg = 'post_id'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'post_id': self.object.id})


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    pk_url_kwarg = 'post_id'

    def has_permission(self):
        return self.get_object().created_by == self.request.user

    def get_success_url(self):
        return reverse('post-detail', kwargs={'post_id': self.object.id})


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_delete_confirm.html"
    pk_url_kwarg = 'post_id'

    def has_permission(self):
        return self.get_object().created_by == self.request.user

    def get_success_url(self):
        return reverse('post-index')
