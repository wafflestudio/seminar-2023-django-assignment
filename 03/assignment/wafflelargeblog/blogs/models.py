from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .managers import UserManager

class User(AbstractUser):
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='posts')

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    
    is_updated = models.BooleanField(default=False)

    def __str__(self):
        return self.content
    
class Tag(models.Model):
    content = models.CharField(primary_key=True, max_length=100)
    post = models.ManyToManyField(Post, related_name='tag', blank=True)

    comment = models.ManyToManyField(Comment, related_name='tag', blank=True)

    def __str__(self):
        return self.content