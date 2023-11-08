from django.shortcuts import render, redirect
from django.http import Http404
from .models import Post, Comment
from .forms import PostForm, CommentForm


def main(request):
    return render(request, "blog/main.html")


def post_list(request):
    posts = Post.objects.all()
    context = {"posts" : posts}
    return render(request, "blog/post_list.html", context=context)


def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post)
    except:
        raise Http404
    if request.method == "POST":
        if "submit" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save()
                new_comment.auther = request.user
                new_comment.post = post
                new_comment.save()
                return redirect("post-detail", post_id=post.id)
        elif "delete" in request.POST:
            pass
    else:
        comment_form = CommentForm()
    context = {"post" : post, "comments" : comments, "form" : comment_form}
    return render(request, "blog/post_detail.html", context=context)


def post_create(request):
    if not request.user.is_authenticated:
        raise Http404
    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save()
            new_post.auther = request.user
            new_post.save()
            return redirect("post-detail", post_id=new_post.id)
    else:
        post_form = PostForm()
    context = {"form" : post_form}
    return render(request, "blog/post_create.html", context=context)


def post_update(request, post_id):
    if not request.user.is_authenticated:
        raise Http404
    try:
        post = Post.objects.get(id=post_id)
    except:
        raise Http404
    
    if request.user != post.auther:
        raise Http404
    if request.method == "POST":
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post = post_form.save()
            return redirect("post-detail", post_id=post.id)
    else:
        post_form = PostForm(instance=post)
    context = {"form" : post_form}
    return render(request, "blog/post_create.html", context=context)


def post_delete(request, post_id):
    if not request.user.is_authenticated:
        raise Http404
    try:
        post = Post.objects.get(id=post_id)
    except:
        raise Http404
    
    if request.user != post.auther:
        raise Http404
    if request.method == "POST":
        if "Yes" in request.POST:
            post.delete()
            return redirect("post-list")
        elif "No" in request.POST:
            return redirect("post-detail", post_id=post.id)
    context = {"post" : post}
    return render(request, "blog/post_delete.html", context=context)