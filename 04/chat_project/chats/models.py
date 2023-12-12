from django.db import models

class Chat(models.Model):
    role = models.CharField(max_length=100, choices=(("assistant", "캐릭터"), ("user", "유저")))
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Character(models.Model):
    image = models.ImageField(upload_to="character-images/")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    first_message = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + self.last_name