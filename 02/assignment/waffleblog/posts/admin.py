from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, User

# Register your models here.

admin.site.register(Post)
admin.site.register(User, UserAdmin)

UserAdmin.fieldsets += ('Custom fields', {'fields': ('nickname',)}),