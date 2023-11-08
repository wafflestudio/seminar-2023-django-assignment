from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from braces.views import LoginRequiredMixin, UserPassesTestMixin

from .models import Post, User, Comment
from .forms import CommentForm, PostForm


# Create your views here.
class PostListView(ListView):
    model = Post
    ordering = ['-dt_created']
    paginate_by = 6
    template_name = 'blog/post_list.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post__id=self.object.id).order_by('-dt_created')
        context['comment_form'] = CommentForm()
        return context

    # def form_valid(self, request):
    #     content = request.POST['content']
    #     author = request.user
    #     post = self.get_object()
    #     new_comment = Comment(content=content, author=author, post=post)
    #     new_comment.save()

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.author = self.request.user
            form.instance.post = self.get_object()
            form.save()
            return redirect('post-detail', pk=self.get_object().id)
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    redirect_unauthenticated_users = True

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    redirect_unauthenticated_users = True
    raise_exception = True

    def test_func(self, user):
        return user == self.get_object().author

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.id})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'

    redirect_unauthenticated_users = True
    raise_exception = True

    def test_func(self, user):
        return user == self.get_object().author

    def get_success_url(self):
        return reverse('post-list')
