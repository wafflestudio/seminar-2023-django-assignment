from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Post(models.Model):
  title = models.CharField(max_length=50, unique=True, error_messages={
    "unique": "There is already a post with the title."
  })
  writer = models.CharField(max_length=50)
  content = models.TextField()
  created_at = models.DateTimeField(verbose_name="Created At", auto_now_add=True)
  updated_at = models.DateTimeField(verbose_name="Updated At", auto_now=True)

  def __str__(self):
    return self.title
  
  # def get_absolute_url(self):
  #   return f"/posts/{self.id}"
  

class User(AbstractUser):
  pass