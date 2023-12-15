from django.db import models

class Character(models.Model):
    image = models.FileField(null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    first_message = models.CharField(max_length=200)

    def get_first_message(self):
        return self.first_message

    def __string__(self):
        name = self.last_name + self.first_name
        return name


class Chat(models.Model):
    ASSISTANT = 'A'
    USER = 'U'

    ROLE_CHOICES = [
        (ASSISTANT, 'assistant'),
        (USER, 'user')
    ]
    role = models.CharField(max_length = 10, choices=ROLE_CHOICES)
    content = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content