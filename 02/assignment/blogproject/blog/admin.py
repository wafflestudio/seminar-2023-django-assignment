
from django.contrib import admin
from .models import Post, Comment

admin.site.register(Post)
admin.site.register(Comment)

#배포 완료