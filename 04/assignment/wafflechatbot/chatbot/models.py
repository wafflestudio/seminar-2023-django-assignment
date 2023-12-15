from django.db import models

# Create your models here.
class Chat(models.Model):
    role = models.CharField(max_length=10, choices=(
        ('assistant', 'character'), ('user', 'user')
    ))
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Character(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.FileField(upload_to='media/')
    first_message = models.CharField(max_length=300)

    def __str__(self):
        return self.first_name + self.last_name