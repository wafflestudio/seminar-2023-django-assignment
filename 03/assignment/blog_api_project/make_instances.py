import random
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_api_project.settings")
django.setup()

from django.core.wsgi import get_wsgi_application
from model_mommy import mommy
from blog.models import Post, Comment, Tag, User
from rest_framework.authtoken.models import Token


mommy.make(User, _quantity=10)

user_ids = []
for user in User.objects.all():
    Token.objects.get_or_create(user=user)
    user_ids.append(user.id)
for i in range(100):
    author = User.objects.get(pk=random.choice(user_ids))
    mommy.make(Post, author=author)

post_ids = []
for post in Post.objects.all():
    post_ids.append(post.id)
for i in range(100):
    author = User.objects.get(pk=random.choice(user_ids))
    post = Post.objects.get(pk=random.choice(post_ids))
    mommy.make(Comment, author=author, post=post)

comment_ids = []
for comment in Comment.objects.all():
    comment_ids.append(comment.id)
for i in range(100):
    post_id_sample = random.sample(post_ids, 3)
    post_set = Post.objects.filter(id__in=post_id_sample)
    comment_id_sample = random.sample(comment_ids, 3)
    comment_set = Comment.objects.filter(id__in=comment_id_sample)
    mommy.make(Tag, posts=post_set, comments=comment_set)
