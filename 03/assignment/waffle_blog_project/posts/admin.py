from django.contrib import admin
from .models import User, Post, Comment, Tag

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)