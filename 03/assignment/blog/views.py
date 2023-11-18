from django.shortcuts import render
from django.views.generic import View, ListView

from .models import Post, Comment, TagPost, TagComment
class IndexView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'
    paginate_by = 8

