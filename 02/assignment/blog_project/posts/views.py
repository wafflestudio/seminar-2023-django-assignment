from django.shortcuts import redirect
from django.views.generic import (
    CreateView, ListView, DetailView, UpdateView, DeleteView, RedirectView
)
from django.urls import reverse
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.
class IndexRedirectView(RedirectView):
    pattern_name = 'post-list'

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.id})
class PostListView(ListView):
    model = Post
    ordering = ['-dt_created']
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = Comment.objects.filter(post=post).order_by('-dt_created')
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(post.get_absolute_url())
        return self.get(request, *args, **kwargs)

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.id})

class PostDeleteView(DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('post-list')