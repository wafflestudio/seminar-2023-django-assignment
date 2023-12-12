from django.db import models

# Create your models here.
from .validators import validate_for_symbols

from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from datetime import timedelta
from django.core.validators import MinLengthValidator

class User(AbstractUser):
   pass

class Tag(models.Model):
   name = models.CharField(max_length=100, unique=True, primary_key=True)

   def __str__(self):
      return self.name
    
class Post(models.Model):
   title = models.CharField(verbose_name = "제목", max_length=50, unique=True, error_messages={'unique' : '유일한 제목을 영어로 하면 unique라고. 뭔가 우월하지 않나?'})
   content = models.TextField(verbose_name = "내용", validators=[MinLengthValidator(5, '5글자 미만의 댓글.. 폭발해라'), validate_for_symbols])

   author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name = "작성자")
   dt_created = models.DateTimeField(verbose_name="작성 시각", auto_now_add=True)
   dt_modified = models.DateTimeField(verbose_name="수정 시각", auto_now=True)

   tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, related_name='posts', verbose_name = "태그")

   def get_absolute_url(self):
      return reverse('posts_detail', kwargs={'pk': self.pk})

   def __str__(self):
      return self.title

class Comment(models.Model):
   content = models.TextField(verbose_name = "내용", max_length = 300, blank = False)
   dt_created = models.DateTimeField(verbose_name="작성 시각", auto_now_add=True)
   dt_updated = models.DateTimeField(verbose_name="수정 시각", auto_now=True)
   author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")

   post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="이 댓글이 달린 글")
   tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, related_name='comments', verbose_name="태그")

   def is_updated(self):
      return self.dt_created + timedelta(seconds = 1) < self.dt_updated

   def __str__(self):
      return self.content[:30]
    