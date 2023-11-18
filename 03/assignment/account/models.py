from django.db import models
from django.contrib.auth.models import AbstractUser	# AbstractUser 불러오기

class User(AbstractUser):
    nickname = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.username