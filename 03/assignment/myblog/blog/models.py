from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    #nickname = models.CharField(max_length = 15, unique=True, null=True)
    def __str__(self):
        return self.username

class Post(models.Model):
    title = models.CharField(max_length=60)
    content = models.TextField(blank=True)
    author = models.CharField(max_length=40)
    dt_created = models.DateField(auto_now_add=True, editable=False)
    dt_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=40)
    content = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True, editable=False)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.content