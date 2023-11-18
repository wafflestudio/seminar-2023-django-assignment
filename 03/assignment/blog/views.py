from braces.views import LoginRequiredMixin

from django.shortcuts import render, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Post, Comment, TagPost, TagComment
from .forms import PostForm, CommentForm


class IndexView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'
    paginate_by = 8


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(post_id=self.object.id)
        return context


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
        return (self.get_object().created_by == self.request.user) or (self.request.user.is_superuser)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'post_id': self.object.id})


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_delete_confirm.html"
    pk_url_kwarg = 'post_id'

    def has_permission(self):
        return (self.get_object().created_by == self.request.user) or (self.request.user.is_superuser)

    def get_success_url(self):
        return reverse('post-index')


class CommentCreateView(LoginRequiredMixin, CreateView):
    http_method_names = ['post']
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.post = Post.objects.get(id=self.kwargs.get('post_id'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'post_id': self.kwargs.get('post_id')})


class CommentUpdateView(PermissionRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"
    pk_url_kwarg = 'comment_id'

    def has_permission(self):
        return (self.get_object().created_by == self.request.user) or (self.request.user.is_superuser)

    def get_success_url(self):
        self.object.is_updated = True
        return reverse('post-detail', kwargs={'post_id': self.object.post.id})


class CommentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_delete_confirm.html"
    pk_url_kwarg = 'comment_id'

    def has_permission(self):
        return (self.get_object().created_by == self.request.user) or (self.request.user.is_superuser)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'post_id': self.object.post.id})
