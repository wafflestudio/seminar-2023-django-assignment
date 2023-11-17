from django.shortcuts import render, redirect
from .models import Article, User, Comment
# Create your views here.
def index(request):
    return render(request, 'wblog/index.html')

def posts(request):
    cur_user = request.user

    if cur_user.is_authenticated:
        user = User.objects.get(username=cur_user.username)

        return render(request, 'wblog/post.html', {'user' : user})
    else:
        return render(request, 'wblog/wrongaccess.html')

def lists(request):
    object_list = Article.objects.all().order_by("dt_created")
    context = {"object_list" : object_list}
    return render(request, 'wblog/list.html', context=context)

def detail(request, pk):
    context = {}
    article = Article.objects.get(id=pk)
    context['article'] = article
    context['user'] = request.user
    context['owner'] = False
    if article.writer == request.user:
        context['owner'] = True

    comments = Comment.objects.all()
    comment_id = []
    for c in comments:
        if c.article == article:
            comment_id.append(c.id)

    comment = Comment.objects.filter(pk__in=comment_id).order_by("dt_created")
    context['comment'] = comment

    return render(request, 'wblog/detail.html', context=context)



def create(request):
    if not request.GET['title']:
        return render(request, 'wblog/wrongarticle.html')

    article = Article()
    article.title = request.GET['title']
    article.text = request.GET['text']
    article.writer = request.user
    article.save()
    return redirect('index')


def edit(request, pk):
    cur_user = request.user
    article = Article.objects.get(id=pk)

    if cur_user != article.writer:
        return render(request, 'wblog/wrongaccess.html')
    
    return render(request, 'wblog/update.html', {"article":article})

def edit_end(request, pk):
    if not request.GET['title']:
        return render(request, 'wblog/wrongarticle.html')

    article = Article.objects.get(id=pk)
    article.title = request.GET['title']
    article.text = request.GET['text']
    article.save()
    return redirect('index')

def add_comment(request, pk):
    comment = Comment()
    comment.writer = request.user
    comment.article = Article.objects.get(id=pk)
    comment.text = request.GET['text']

    comment.save()
    return detail(request, pk)


def delete(reqeust, pk):
    Comment.objects.filter(article__id=pk).delete()
    Article.objects.get(id=pk).delete()
    return redirect('index')