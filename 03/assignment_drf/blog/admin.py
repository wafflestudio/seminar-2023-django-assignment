from django.contrib import admin
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple

from .models import Post, Comment, Tag


class CommentInline(admin.StackedInline):
    model = Comment
class TagPostInline(admin.StackedInline):
    model = Tag.post.through
class TagCommentInline(admin.StackedInline):
    model = Tag.comment.through

class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
        TagPostInline,
    ]
    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple}
    }
class CommentAdmin(admin.ModelAdmin):
    inlines = [
        TagCommentInline,
    ]
    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple}
    }
class TagAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple}
    }


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)
