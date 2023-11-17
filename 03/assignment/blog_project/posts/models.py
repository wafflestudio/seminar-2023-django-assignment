from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from rest_framework.authtoken.models import Token


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128, verbose_name='password')
    def __str__(self):
        return self.username

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Post(models.Model):
    title = models.CharField(max_length=50, unique=True,
                                error_messages={'unique': '같은 제목의 글을 쓸 수 없습니다.'})
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Date updated", auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_updated = (created_at != updated_at)

    def __str__(self):
        return self.content
