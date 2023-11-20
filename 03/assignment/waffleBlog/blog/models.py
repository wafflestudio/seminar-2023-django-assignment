from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Tag(models.Model):
    content = models.CharField(unique=True, primary_key=True, max_length=100)

    def __str__(self):
        return self.content


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='posts')

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "글"
        verbose_name_plural = "글 목록"


class Comment(models.Model):
    description = models.CharField(max_length=300)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_updated = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name='comments')

    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"

    def save(self, *args, **kwargs):
        # 댓글이 수정될 때 is_updated 필드를 True로 설정
        if self.pk:
            self.is_updated = True
        super().save(*args, **kwargs)
