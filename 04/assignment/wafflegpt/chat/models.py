from django.db import models

# Create your models here.
class Chat(models.Model):
    role = models.CharField(max_length=200, choices=(
        ("assistant", '캐릭터'), ("user", '유저')
    ))
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

class Character(models.Model):
    #image = models.URLField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.FileField(upload_to='media/')
    first_message = models.CharField(max_length=300)