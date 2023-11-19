# posts/models.py
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128, verbose_name='password')

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Tag(models.Model):
    content = models.CharField(max_length=30, primary_key=True, unique=True)

    def __str__(self):
        return self.content

    def can_delete(self ):
        # Check if this tag is used by any Post or Comment
        used_in_posts = Post.objects.filter(tags=self).exists()
        used_in_comments = Comment.objects.filter(comment_tags=self).exists()

        # Return True if not used in any Post or Comment, else False
        return not used_in_posts and not used_in_comments


def delete_unused_tags():
    for tag in Tag.objects.all():
        #print("Checking tag", tag)
        if tag.can_delete():
            tag.delete()


class Post(models.Model):
    title = models.CharField(max_length=50, unique=True, error_messages={'unique': '같은 제목의 글을 쓸 수 없습니다.'})
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Date updated", auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, help_text="태그는 해시태그(#)로 분리해서 적어주세요.")

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)
        delete_unused_tags()


class Comment(models.Model):
    content = models.TextField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_updated = models.BooleanField(default=False)
    comment_tags = models.ManyToManyField(Tag, blank=True, help_text="태그는 해시태그(#)로 분리해서 적어주세요.")

    def __str__(self):
        return self.content

    def delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)
        delete_unused_tags()
