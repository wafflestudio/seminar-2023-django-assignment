from django.db import models

# Create your models here.

class Character(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    first_message = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Chat(models.Model):
    role = models.CharField(max_length=50, choices=(
        ("assistant", "assistant"), ("user", "user")
    ))
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

