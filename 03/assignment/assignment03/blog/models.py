from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __str__(self):
        return self.username
    

class Tag(models.Model):
    content = models.CharField(name="content", max_length=50, primary_key=True)
    
    def __str__(self):
        return self.content


class Post(models.Model):
    created_by = models.ForeignKey(User, name="created_by", null=True, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(name="created_at", auto_now_add=True)
    updated_at = models.DateTimeField(name="updated_at", auto_now=True)
    title = models.CharField(name="title", max_length=100)
    description = models.TextField(name="description")
    tags = models.ManyToManyField(Tag, name="tags", related_name="posts", blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-created_at"]
    

class Comment(models.Model):
    post = models.ForeignKey(Post, name="post", on_delete=models.CASCADE, related_name="comments")
    created_by = models.ForeignKey(User, name="created_by", on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(name="created_at", auto_now_add=True)
    updated_at = models.DateTimeField(name="updated_at", auto_now=True)
    content = models.TextField(name="content")
    is_updated = models.BooleanField(name="is_updated")
    tags = models.ManyToManyField(Tag, name="tags", related_name="comments", blank=True)
    def __str__(self):
        return "comment by " + self.created_by.__str__()
    
    class Meta:
        ordering = ["-created_at"]


