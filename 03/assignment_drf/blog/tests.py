from django.test import TestCase

from .models import Post,Comment
from model_mommy import mommy
from account.models import User

import random
def create_posts(number):
    for _ in range(number):

        user_id = random.randint(1,20)
        while not User.objects.filter(id=user_id).exists():
            user_id = random.randint(1, 20)

        mommy.make('Post', created_by=User.objects.get(id=user_id))
def create_comments(number):
    for _ in range(number):
        user_id = random.randint(1,20)
        post_id = random.randint(20,100)
        while not User.objects.filter(id=user_id).exists():
            user_id = random.randint(1, 20)
        while not Post.objects.filter(id=post_id).exists():
            post_id = random.randint(20,100)

        mommy.make('Comment', created_by=User.objects.get(id=user_id), post=Post.objects.get(id=post_id))


