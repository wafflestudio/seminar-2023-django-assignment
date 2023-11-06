from django.shortcuts import render, redirect
from django.urls import reverse
from allauth.account.views import PasswordChangeView
from .forms import PageForm, CommentForm
from .models import Post, Comment
from django.utils import timezone
# Create your views here.
def index(request):
    return render(request, "blog/index.html")

class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse("index")

def page_create(request):
    if request.method == 'POST':
        new_page = Post(
            title=request.POST['title'],
            content=request.POST['content'],
            #author=request.POST['author'],
            author=request.user.username,
            dt_created=timezone.now(),
            dt_updated=timezone.now()
        )
        new_page.save()
        return redirect('page-detail', page_id=new_page.id)
    else:
        form = PageForm()
        return render(request, 'blog/page_form.html', {'form':form})

def page_detail(request, page_id):
    object = Post.objects.get(id=page_id)
    return render(request, 'blog/page_detail.html', {'object': object})

def page_list(request):
    object_list = Post.objects.all()  # 데이터 조회
    return render(request, 'blog/page_list.html', {'object_list': object_list})


def main_page(request):
    return render(request, 'blog_base/base.html')

def page_update(request, page_id):
    object = Post.objects.get(id=page_id)
    if request.method == 'POST':
        form = PageForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect('page-detail', page_id=object.id)
    else:
        form = PageForm(instance=object)
    return render(request, 'blog/page_form.html', {'form': form})


def page_delete(request, page_id):
    object = Post.objects.get(id=page_id)
    if request.method == 'POST':
        object.delete()
        return redirect('page-list')
    else:
        return render(request, 'blog/page_confirm_delete.html', {'object': object})


def comments_create(request, page_id):
    if request.method == 'POST':
        comments = Comment.objects.all()
        curpost = Post.objects.get(id=page_id)
        new_comment = Comment(
            post = curpost,
            #author=request.POST['author'],
            author = request.user.username,
            content=request.POST['content'],
            created_at=timezone.now,
            updated_at=timezone.now
        )
        new_comment.save()
        #return redirect('page-detail', page_id=curpost.id)
        return render(request, 'blog/page_detail.html', {'object':curpost, 'comments':comments})
    else:
        form = CommentForm()
        return render(request, 'blog/page_form.html', {'form': form})



def comments_delete(request, page_id, comment_id):
    if request.user.is_authenticated:
        comment = Comment.objects.get(id=comment_id)
        #if request.user == comment.author:
        comment.delete()
    return redirect('page-detail', page_id)