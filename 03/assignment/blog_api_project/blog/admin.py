from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Comment, Tag


class CommentInline(admin.StackedInline):
    model = Comment


class TagToPostInline(admin.StackedInline):
    model = Tag.posts.through
    verbose_name = 'Tag'
    verbose_name_plural = 'Tags'


class TagToCommentInline(admin.StackedInline):
    model = Tag.comments.through
    verbose_name = 'Tag'
    verbose_name_plural = 'Tags'


class CommentAdmin(admin.ModelAdmin):
    inlines = (
        TagToCommentInline,
    )


class PostAdmin(admin.ModelAdmin):
    inlines = (
        CommentInline,
        TagToPostInline,
    )


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag)
