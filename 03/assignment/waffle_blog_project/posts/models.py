from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=25, unique=True)

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
        used_in_posts = Post.objects.filter(tags=self).exists()
        used_in_comments = Comment.objects.filter(comment_tags=self).exists()
        return not used_in_posts and not used_in_comments


def delete_unused_tags():
    for tag in Tag.objects.all():
        if tag.can_delete():
            tag.delete()

class Post(models.Model):
    title = models.CharField(max_length=60, unique=True, error_messages={
        'unique': 'This post title already exists.'
        })
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, help_text='Please separate your tags with #')

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)
        delete_unused_tags()

class Comment(models.Model):
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True, help_text='Please separate your tags with #')

    def __str__(self):
        return self.content

    def delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)
        delete_unused_tags()

