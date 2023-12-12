from braces.views import LoginRequiredMixin

from django.shortcuts import render, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q

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
        context['tags'] = self.object.tagPost.filter(post=self.object)
        context['ctags'] = TagComment.objects.filter(comment__post=self.object)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    add_tags = []

    def post(self, request, *args, **kwargs):
        tag_text = self.request.POST.get("TagPost")
        if tag_text:
            ptags = [ptag.strip() for ptag in tag_text.split(",")]
            for ptag in ptags:
                tag, _ = TagPost.objects.get_or_create(content=ptag)
                self.add_tags.append(tag)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        for tag in self.add_tags:
            self.object.tagPost.add(tag)
        return reverse('post-detail', kwargs={'post_id': self.object.id})


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    pk_url_kwarg = 'post_id'
    update_tags = list()

    def post(self, request, *args, **kwargs):
        tag_text = self.request.POST.get("TagPost")
        self.update_tags = []
        if tag_text:
            ptags = [ptag.strip() for ptag in tag_text.split(",")]
            for ptag in ptags:
                tag, _ = TagPost.objects.get_or_create(content=ptag)
                self.update_tags.append(tag)
        return super().post(request, *args, **kwargs)

    def has_permission(self):
        return (self.get_object().created_by == self.request.user) or (self.request.user.is_superuser)

    def get_success_url(self):
        old_tags = [old_tag.content for old_tag in self.object.tagPost.filter(post=self.object)]
        for old_tag in old_tags:
            if old_tag not in self.update_tags:
                tag = TagPost.objects.get(content=old_tag)
                self.object.tagPost.remove(tag)
                if not Post.objects.filter(tags__content=old_tag).exists():
                    TagPost.objects.get(content=old_tag).delete()
        for update_tag in self.update_tags:
            if update_tag not in old_tags:
                tag, _ = TagPost.objects.get_or_create(content=update_tag)
                self.object.tagPost.add(tag)
        return reverse('post-detail', kwargs={'post_id': self.object.id})


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_delete_confirm.html"
    pk_url_kwarg = 'post_id'

    def has_permission(self):
        return (self.get_object().created_by == self.request.user) or (self.request.user.is_superuser)

    def get_success_url(self):
        old_tags = [old_tag.content for old_tag in self.object.tagPost.filter(post=self.object)]
        for old_tag in old_tags:
            tag = TagPost.objects.get(content=old_tag)
            self.object.tagPost.remove(tag)

        post_tags = [tag.content for tag in TagPost.objects.all()]
        for post_tag in post_tags:
            if not Post.objects.filter(tags__content=post_tag).exists():
                TagPost.objects.get(content=post_tag).delete()
        return reverse('post-index')


class CommentCreateView(LoginRequiredMixin, CreateView):
    http_method_names = ['post']
    model = Comment
    form_class = CommentForm
    add_tags = []

    def post(self, request, *args, **kwargs):
        tag_text = self.request.POST.get("TagComment")
        if tag_text:
            ctags = [ctag.strip() for ctag in tag_text.split(",")]
            for ctag in ctags:
                tag, _ = TagComment.objects.get_or_create(content=ctag)
                self.add_tags.append(tag)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.post = Post.objects.get(id=self.kwargs.get('post_id'))
        return super().form_valid(form)

    def get_success_url(self):
        for tag in self.add_tags:
            self.object.tagComment.add(tag)
        return reverse('post-detail', kwargs={'post_id': self.kwargs.get('post_id')})


class CommentUpdateView(PermissionRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"
    pk_url_kwarg = 'comment_id'
    update_tags = list()

    def post(self, request, *args, **kwargs):
        tag_text = self.request.POST.get("TagComment")
        self.update_tags = []
        if tag_text:
            ctags = [ctag.strip() for ctag in tag_text.split(",")]
            for ctag in ctags:
                tag, _ = TagComment.objects.get_or_create(content=ctag)
                self.update_tags.append(tag)
        return super().post(request, *args, **kwargs)

    def has_permission(self):
        return (self.get_object().created_by == self.request.user) or (self.request.user.is_superuser)

    def get_success_url(self):
        self.object.is_updated = True
        old_tags = [old_tag.content for old_tag in self.object.tagComment.filter(comment=self.object)]
        for old_tag in old_tags:
            if old_tag not in self.update_tags:
                tag = TagComment.objects.get(content=old_tag)
                self.object.tagComment.remove(tag)
                if not Comment.objects.filter(tags__content=old_tag).exists():
                    TagComment.objects.get(content=old_tag).delete()
        for update_tag in self.update_tags:
            if update_tag not in old_tags:
                tag, _ = TagComment.objects.get_or_create(content=update_tag)
                self.object.tagComment.add(tag)
        return reverse('post-detail', kwargs={'post_id': self.object.post.id})


class CommentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_delete_confirm.html"
    pk_url_kwarg = 'comment_id'

    def has_permission(self):
        return (self.get_object().created_by == self.request.user) or (self.request.user.is_superuser)

    def get_success_url(self):
        old_tags = [old_tag.content for old_tag in self.object.tagComment.filter(comment=self.object)]
        for old_tag in old_tags:
            tag = TagComment.objects.get(content=old_tag)
            self.object.tagComment.remove(tag)

        comment_tags = [tag.content for tag in TagComment.objects.all()]
        for comment_tag in comment_tags:
            if not Comment.objects.filter(tags__content=comment_tag).exists():
                TagComment.objects.get(content=comment_tag).delete()
        return reverse('post-detail', kwargs={'post_id': self.object.post.id})


class SearchPostView(ListView):
    model = Post
    context_object_name = 'search_post'
    template_name = 'blog/search_post.html'
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Post.objects.filter(tags__content__icontains=query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        return context


class SearchCommentView(ListView):
    model = Comment
    context_object_name = 'search_comment'
    template_name = 'blog/search_comment.html'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Comment.objects.filter(tags__content__icontains=query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        return context
