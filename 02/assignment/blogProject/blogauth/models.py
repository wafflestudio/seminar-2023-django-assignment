from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class User(AbstractUser):
   objects = UserManager()