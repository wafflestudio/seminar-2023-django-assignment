from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import PostForm, SignupForm, CommentForm
from braces.views import LoginRequiredMixin

# Create your views here.

def index(request):
    print(request.user.is_authenticated)
    return render(request, "posts/index.html")

def posts_list(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "posts/posts_list.html", context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.filter(post=post)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return redirect("post_detail", post_id=post.id)
    else:
        comment_form = CommentForm()
        context = {"post": post, "comment": comment, "form": comment_form}
        return render(request, "posts/post_detail.html", context)


def post_create(request):
    if not request.user.is_authenticated:
        return redirect("posts_list")
    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save()
            post.save()
        return redirect("post_detail", post_id=post.id)
    else:
        post_form = PostForm()
        return render(request, 'posts/post_form.html', {'form': post_form })
    

def post_update(request, post_id):
    post = Post.objects.get(id=post_id)
    if not request.user.is_authenticated:
        return redirect("post_detail", post_id=post.id)
    if request.method == "POST":
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post = post_form.save()
        return redirect("post_detail", post_id=post.id)
    else:
        post_form = PostForm(instance=post)
        return render(request, 'posts/post_form.html', {'form': post_form })
    

def post_delete(request, post_id):
    post = Post.objects.get(id=post_id)
    if not request.user.is_authenticated:
        return redirect("post_detail", post_id=post.id)
    if request.method == 'POST':
        post.delete()
        return redirect("posts_list")
    else: 
        return render(request, 'posts/post_confirm_delete.html', {'post': post})
    

def change_profile(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.signup(request, form)
            return redirect("index")
    else:
        form = SignupForm()
        return render(request, 'posts/change_profile.html', {'form': form})