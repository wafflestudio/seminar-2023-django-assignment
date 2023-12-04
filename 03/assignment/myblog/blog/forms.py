from django import forms
from .models import Post, Comment
class PageForm(forms.ModelForm):
    tags_input = forms.CharField(max_length=200, required=False)
    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'dt_created', 'dt_updated', 'tags_input']
        exclude = ('author', 'dt_created', 'dt_updated',)

class CommentForm(forms.ModelForm):
    tags_input = forms.CharField(max_length=200, required=False)
    class Meta:
        model = Comment
        fields = ['post', 'author', 'content', 'created_at', 'updated_at', 'tags_input']
        exclude = ('post', 'author', 'created_at', 'updated_at')