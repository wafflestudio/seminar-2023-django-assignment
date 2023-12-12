from django.contrib import admin
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple

from .models import Post, Comment, TagPost, TagComment


class CommentInline(admin.StackedInline):
    model = Comment
class TagPostInline(admin.StackedInline):
    model = TagPost.post.through
class TagCommentInline(admin.StackedInline):
    model = TagComment.comment.through


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
class TagPostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple}
    }
class TagCommentAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple}
    }


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(TagPost, TagPostAdmin)
admin.site.register(TagComment, TagCommentAdmin)
