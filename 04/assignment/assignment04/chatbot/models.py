from django.db import models

class RoleChoices(models.TextChoices):
    ASSISTANT = "assistant"
    USER = "user"


class Character(models.Model):
    image = models.ImageField(name="image", upload_to='chatbot/static/chatbot/', max_length=100, default="chatbot/static/chatbot/bonobono.png")
    first_name = models.CharField(name="first_name", max_length=100)
    last_name = models.CharField(name="last_name", max_length=100)


class Chat(models.Model):
    role = models.CharField(name="role", choices=RoleChoices.choices, max_length=100)
    content = models.CharField(name="content", max_length=100)
    created_at = models.DateTimeField(name="created_at", auto_now_add=True)