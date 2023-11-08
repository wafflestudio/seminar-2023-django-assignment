from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from .validators import validate_symbols
from django.urls import reverse
# Create your models here.


class User(AbstractUser):
    pass

class Post(models.Model):
    #  글의 제목, 내용, 작성일, 마지막 수정일
    title = models.CharField(max_length=50, unique=True,
                            error_messages={'unique':'이미 있는 제목입니당'})
    content = models.TextField(validators=[MinLengthValidator(10, '10글자 이상 작성해주세요'),
                                        validate_symbols])
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    dt_created = models.DateTimeField(verbose_name="Date Created", auto_now_add=True)
    dt_modified = models.DateTimeField(verbose_name="Date modified", auto_now=True)
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content = models.TextField(max_length=500, blank = False)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.content[:30]