from django.db import models

# Create your models here.

class Character(models.Model):
    image = models.TextField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Chat(models.Model):
    role = models.CharField(max_length=10)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
