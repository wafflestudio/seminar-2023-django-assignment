from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Comment, Tag, Profile

# Register your models here.
admin.site.register(User, UserAdmin)
#UserAdmin.fieldsets += ("Custom fields", {"fields":("nickname",)})
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Profile)