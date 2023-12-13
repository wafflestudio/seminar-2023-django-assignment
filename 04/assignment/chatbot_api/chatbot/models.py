from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Character(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    image = models.ImageField(blank=True, null=True)
    first_message = models.CharField(max_length=100)

    def __str__(self):
        return self.last_name + self.first_name


# Create your models here.

class Chat(models.Model):
    ROLE_CHOICES = [
        ('system', 'system'),
        ('user', 'user'),
        ('assistant', 'assistant'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    content = models.TextField()

    dt_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['dt_created']

    def __str__(self):
        return self.content[:30]

