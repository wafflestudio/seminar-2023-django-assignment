from django.db import models


class Character(models.Model):
    image = models.ImageField()
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)


class Chat(models.Model):
    ROLE_CHOICES = [
        ('assistant', 'Assistant'),
        ('user', 'User'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
