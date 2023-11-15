from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import validate_no_special_characters

class User(AbstractUser):

    def __str__(self):
        return self.email

class Post(models.Model):
    title = models.CharField(max_length=30)
    
    content = models.TextField()
    
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-dt_created']


class Comment(models.Model):
    content = models.TextField(max_length=500, blank=False)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.content[:30]
    
    class Meta:
        ordering = ['-dt_created']
