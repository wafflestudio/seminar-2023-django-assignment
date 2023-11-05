from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.
class PostCreateView(CreateView):
   template_name = "blog/post_create.html"
   model = Post
   form_class = PostForm
   success_url = reverse_lazy("post_list")

   def form_valid(self, form):
      self.object = form.save(commit = False)
      self.object.created_by = self.request.user
      self.object.save()
      return super().form_valid(form)

class PostListView(ListView):
   template_name = "blog/post_list.html"
   model = Post
   context_object_name = 'posts'  #템플릿 파일에서 posts로 받을 것을 의미함
   paginated_by = 10 # 1페이지에 10개씩
   orderling = ['-updated_at'] # 내림차순 정렬

class PostDetailView(DetailView):
   template_name = "blog/post_detail.html"
   model = Post
   context_object_name = 'object'

   def get_context_data(self, **kwargs):
      return {**super().get_context_data(**kwargs), "forms": CommentForm(), "comments": self.object.comments.all()}
   
   def post(self, request, *args, **kwargs):
      self.object = self.get_object()
      form = CommentForm(request.POST)
      
      if form.is_valid():
         comment = form.save(commit=False)
         comment.post = self.object
         comment.created_by = self.request.user
         comment.save()
         return HttpResponseRedirect(self.get_success_url())
      else:
         return self.render_to_response(self.get_context_data(form=form))

   def get_success_url(self):
      return reverse('post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(DeleteView):
   model = Post
   template_name = 'blog/post_confirm_delete.html'

   def get_success_url(self):
      return reverse('post_list')

class PostUpdateView(UpdateView):
   template_name = 'blog/post_edit.html'
   model = Post
   form_class = PostForm

   def get_success_url(self):
      return reverse('post_detail', kwargs={'pk': self.object.id})

class CommentDeleteView(DeleteView):
   template_name = 'blog/comment_confirm_delete.html'
   model = Comment

   def get_success_url(self):
      return reverse('post_detail', kwargs={'pk': self.object.post.id})

class CommentUpdateView(UpdateView):
   template_name = 'blog/comment_edit.html'
   model = Comment
   form_class = CommentForm

   def get_success_url(self):
      return reverse('post_detail', kwargs={'pk': self.object.post.id})

## UpdateView : 템플릿(.html)에서는 object로 객체를 받음