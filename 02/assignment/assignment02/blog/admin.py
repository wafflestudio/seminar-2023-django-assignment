from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Comment

# Register your models here.
admin.site.register(User, UserAdmin)
UserAdmin.fieldsets += (("Custom fields", {"fields": ("nickname", )}), )
class ProjectsInLine(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Post)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ("title", )

    search_fields = ["user__username"]

    inlines = [
        ProjectsInLine
    ]

    def _projects(self, obj):
        return obj.projects.all().count()