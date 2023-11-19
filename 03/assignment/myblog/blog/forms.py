from django import forms
from .models import Post, Comment
class PageForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'dt_created', 'dt_updated']
        exclude = ('author', 'dt_created', 'dt_updated',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['post', 'author', 'content', 'created_at', 'updated_at']
        exclude = ('post', 'author', 'created_at', 'updated_at')