from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
  nickname = models.CharField(max_length=20, unique=True, default="User", error_messages={
    "unique": "There is already a user with the nickname."
  })

  def __str__(self):
    return self.email

class Post(models.Model):
  title = models.CharField(max_length=50, unique=True, error_messages={
    "unique": "There is already a post with the title."
  })
  content = models.TextField()
  created_at = models.DateTimeField(verbose_name="Created At", auto_now_add=True)
  updated_at = models.DateTimeField(verbose_name="Updated At", auto_now=True)

  def __str__(self):
    return self.title

class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
  content = models.TextField()
  created_at = models.DateTimeField(verbose_name="Created At", auto_now_add=True)
  updated_at = models.DateTimeField(verbose_name="Updated At", auto_now=True)

  def __str__(self):
    return self.content