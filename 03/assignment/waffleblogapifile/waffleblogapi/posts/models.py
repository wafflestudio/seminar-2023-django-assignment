from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
  pass

class Tag(models.Model):
  content = models.CharField(max_length=50, primary_key=True, default= '',unique=True, error_messages={
    "unique": "There is already a tag with the content."
  })
  

class Post(models.Model):
  title = models.CharField(max_length=50, unique=True, error_messages={
    "unique": "There is already a post with the title."
  })
  tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
  author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  content = models.TextField()
  created_at = models.DateTimeField(verbose_name="Created At", auto_now_add=True)
  updated_at = models.DateTimeField(verbose_name="Updated At", auto_now=True)

  def __str__(self):
    return self.title

class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
  tags = models.ManyToManyField(Tag, blank=True, related_name="comments")
  author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  updated = models.BooleanField(default=False)
  content = models.TextField()
  created_at = models.DateTimeField(verbose_name="Created At", auto_now_add=True)
  updated_at = models.DateTimeField(verbose_name="Updated At", auto_now=True)

  def __str__(self):
    return self.content