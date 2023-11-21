from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']

    tags = forms.CharField(max_length=200)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
