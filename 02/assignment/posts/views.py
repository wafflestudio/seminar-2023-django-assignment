from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.views.generic import ListView

def gomainpage(request):
    redirect('index')

"""def index(request):
    postings = Post.objects.all()
    contents = dict()
    contents["posts"] = postings
    contents["user"] = request.user
    return render(request, "posts/index.html", context=contents)"""
class IndexView(ListView):
    model = Post
    template_name = "posts/index.html"
    context_object_name = "posts"
    paginate_by = 5
    ordering = ["-dt_created"]


def detailView(request, post_id):
    posting = Post.objects.get(id=post_id)
    if request.method == 'POST':
        comment_content = request.POST["content"]
        Comment.objects.create(post=posting, content=comment_content, author=request.user)
    contents = dict()
    contents["post"] = posting
    contents["comments"] = Comment.objects.filter(post_id=post_id)
    return render(request, 'posts/post_detail.html', context=contents)

@login_required
def createView(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        newPost = Post.objects.create(title=title, content=content, author=request.user)
        return redirect(f"/posts/{newPost.id}/")
    return render(request, "posts/post_form.html")

@login_required
def updateView(request, post_id):
    if request.method == 'POST':
        uppost = Post.objects.get(id = post_id)
        uppost.title = request.POST['title']
        uppost.content = request.POST['content']
        uppost.save()
        return redirect(f"/posts/{uppost.id}/")
    else:
        post = Post.objects.get(id=post_id)
        contents = dict()
        contents["post_o"] = post
    return render(request, "posts/post_update.html", context=contents)

@login_required
def deleteView(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('index')
    else:
        return render(request, 'posts/post_confirm_delete.html', {'post': post})

@login_required
def commentUpdate(request, post_id, comment_id):
    upcomment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        upcomment.content = request.POST['content']
        upcomment.save()
        return redirect(f"/posts/{post_id}")
    else:
        contents = dict()
        contents["comment_o"] = upcomment
        contents["pid"] = post_id
    return render(request, 'posts/comment_update.html', context=contents)

@login_required
def commentDelete(request, post_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect(f'/posts/{post_id}')
    else:
        return render(request, 'posts/comment_confirm_delete.html', {'comment':comment})