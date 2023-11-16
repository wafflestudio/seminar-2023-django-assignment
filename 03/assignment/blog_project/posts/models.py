from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.
class User(AbstractUser):
    pass


class Post(models.Model):
    title = models.CharField(max_length=50, unique=True,
                                error_messages={'unique': '같은 제목의 글을 쓸 수 없습니다.'})
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Date updated", auto_now=True)

    def get_absolute_url(self):
         return reverse('post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return {self.title + self.description[:300]}


class Comment(models.Model):
    content = models.TextField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_upated = (created_at != updated_at)

    def __str__(self):
        return self.content
