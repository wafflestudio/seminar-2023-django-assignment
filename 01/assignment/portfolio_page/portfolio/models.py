from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    content = models.TextField()
    profile_image_source = models.CharField(max_length=255)
    github_link = models.CharField(max_length=255)

    def __str__(self):
        return self.name