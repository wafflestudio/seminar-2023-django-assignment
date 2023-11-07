from django.shortcuts import render, redirect
from .models import Post, Comment
def index(request):
    postings = Post.objects.all()
    contents = dict()
    contents["posts"] = postings
    return render(request, "posts/index.html", context=contents)

def detailView(request, post_id):
    posting = Post.objects.get(id=post_id)
    contents = dict()
    contents["post"] = posting
    contents["comments"] = Comment.objects.filter(post_id=post_id)
    return render(request, 'posts/post_detail.html', context=contents)

def createView(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        post = Post.objects.create(title=title, content=content, author=request.user)
        return redirect(f"/posts/{post.id}")
    else:
        return render(request, "posts/post_form.html")