from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
  pass

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
  post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
  content = models.TextField()
  created_at = models.DateTimeField(verbose_name="Created At", auto_now_add=True)
  updated_at = models.DateTimeField(verbose_name="Updated At", auto_now=True)

  def __str__(self):
    return self.content