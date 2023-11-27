from django.db import models
from django.db.models.signals import pre_delete, post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token

class User(AbstractUser):
    email = models.EmailField(blank=True, null=True)
    
    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.username

class Post(models.Model):
    title = models.CharField(max_length=30)
    
    content = models.TextField()
    
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    tags = models.ManyToManyField('Tag', related_name='posts')

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-dt_created']


class Comment(models.Model):
    content = models.TextField(max_length=100, blank=False)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField(default=False)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    tags = models.ManyToManyField('Tag', related_name='comments')

    def save(self, *args, **kwargs):
        if self.dt_created!=self.dt_updated:
            self.is_updated = True
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.content[:30]
    
    class Meta:
        ordering = ['-dt_created']

class Tag(models.Model):
    content = models.CharField(max_length=20, blank=False, unique=True, primary_key=True)
    def __str__(self):
        return self.content
    class Meta:
        ordering = ['content']

@receiver(pre_delete, sender=Comment)
def delete_empty_tags(sender, instance, **kwargs):
    for tag in Tag.objects.all():
        if tag.comments.count()==0 and tag.posts.count()==0:
            tag.delete()

@receiver(pre_delete, sender=Post)
def delete_empty_tags(sender, instance, **kwargs):
    for tag in Tag.objects.all():
        if tag.comments.count()==0 and tag.posts.count()==0:
            tag.delete()

@receiver(post_delete, sender=Comment)
def delete_empty_tags(sender, instance, **kwargs):
    for tag in Tag.objects.all():
        if tag.comments.count()==0 and tag.posts.count()==0:
            tag.delete()
            
@receiver(post_delete, sender=Post)
def delete_empty_tags(sender, instance, **kwargs):
    for tag in Tag.objects.all():
        if tag.comments.count()==0 and tag.posts.count()==0:
            tag.delete()

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=Post)
def delete_empty_tags(sender, instance, **kwargs):
    for tag in Tag.objects.all():
        if tag.comments.count()==0 and tag.posts.count()==0:
            tag.delete()
            
@receiver(post_save, sender=Comment)
def delete_empty_tags(sender, instance, **kwargs):
    for tag in Tag.objects.all():
        if tag.comments.count()==0 and tag.posts.count()==0:
            tag.delete()