from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Comment, Article

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Comment)
admin.site.register(Article)

UserAdmin.fieldsets += (("Custom fields", {"fields" : ("nickname",)}),)
