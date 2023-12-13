from django.db import models

# Create your models here.

class Character(models.Model):
    image = models.ImageField(upload_to='bot/chracters/images/')
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.last_name+self.first_name

class Chat(models.Model):
    RoleType = models.TextChoices('assistant','user')
    
    role = models.CharField(max_length = 10,blank=False, choices=RoleType.choices)
    content = models.TextField(max_length=100, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
    class Meta:
        ordering = ['created_at']