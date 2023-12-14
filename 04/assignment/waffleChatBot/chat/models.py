from django.db import models

# Create your models here.

class Character(models.Model):
    image = models.FileField(upload_to='media/', blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Chat(models.Model):
    ROLE_CHOICES = [
        ('assistant', 'assistant'),
        ('user', 'user'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content