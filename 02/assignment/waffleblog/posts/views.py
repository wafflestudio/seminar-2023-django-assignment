from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm, DeleteForm

# Create your views here.


def posts_list(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "posts/posts_list.html", context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {"post": post}
    return render(request, "posts/post_detail.html", context)


def post_create(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save()
        return redirect("post_detail", post_id=post.id)
    else:
        post_form = PostForm()
        return render(request, 'posts/post_form.html', {'form': post_form })
    

def post_update(request, post_id):
    post = Post.objects.get(id=post_id)
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
    if request.method == 'POST':
        post.delete()
        return redirect("posts_list")
    else: 
        return render(request, 'posts/post_confirm_delete.html', {'post': post})
    