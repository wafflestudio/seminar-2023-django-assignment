from django import forms
from .models import Post, User, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    def signup(self, request, user):
        user = super().save()
        return user
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
