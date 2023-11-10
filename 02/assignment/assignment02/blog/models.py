from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_no_special_characters, title_validator, content_validator

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(
        max_length=15, 
        unique=True, 
        null=True, 
        validators=[validate_no_special_characters], 
        error_messages = {"unique": "이미 사용중인 닉네임입니다. "}
    )

    def __str__(self):
        if isinstance(self.nickname, str):
            return self.nickname
        else:
            return "None"


class Post(models.Model):
    title = models.CharField(max_length=80, name="title", null=True, blank=True, validators=[title_validator])
    content = models.TextField(name="content", null=True, blank=True, validators=[content_validator])
    created_date = models.DateTimeField(name="created_date", auto_now_add=True)
    updated_date = models.DateTimeField(name="updated_date", auto_now=True)
    auther = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def title_for_list(self):
        if self.title and len(self.title) > 30:
            return self.title[:30] + '...'
        else:
            return self.title


    def __str__(self):
        if self.title:
            return self.title
        else:
            return "None"
    
class Comment(models.Model):
    content = models.TextField(name="content", validators=[content_validator])
    created_date = models.DateTimeField(name="created_date", auto_now_add=True)
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    auther = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.auther.__str__()