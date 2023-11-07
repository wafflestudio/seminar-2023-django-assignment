from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Post,Comment
from .forms import PostForm, CommentForm
from django.utils import timezone
# Create your views here.
def post_list(request):
    posts = Post.objects.all()
    context= {"posts": posts}
    return render(request, 'blog/post_list.html', context)

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {'post':post}
    return render(request, 'blog/post_detail.html', context)

def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

     #게시물 삭제를 확인하기 위해 GET 요청으로 삭제 페이지를 보여줍니다.
    if request.method == 'GET':
        return render(request, 'blog/post_delete_confirm.html', {'post': post})

    # POST 요청으로 게시물을 삭제합니다.
    if request.method == 'POST':
        post.delete()
        return redirect('/posts/')

#def post_delete(request, post_id):
    #post = get_object_or_404(Post, id=post_id)

    # 글 작성자와 현재 로그인한 사용자를 비교
    #if post.author == request.user:
    #    post.delete()
        return redirect('post-list')
    #else:
        # 권한이 없는 경우에 대한 처리
        return HttpResponse("글을 삭제할 권한이 없습니다.")


def post_write(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():        
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post-list')
    else:
        form = PostForm()
    return render(request, 'blog/post_write.html', {'form':form})


def comment_write(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = Comment(post=post, content=request.POST.get('content'),created_at=timezone.now(), user=request.user)
    comment.save()
    return redirect('blog:post-detail', post_id)

def post_update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post-detail', post_id=post_id)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_update.html', {'form': form, 'post': post})