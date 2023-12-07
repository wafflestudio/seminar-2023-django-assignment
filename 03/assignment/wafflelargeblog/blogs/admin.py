from django.contrib import admin
from django.contrib.auth.admin import UserAdmin #admin이 필요함
from .models import User, Post

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post)