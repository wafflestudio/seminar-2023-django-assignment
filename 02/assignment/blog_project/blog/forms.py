from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {'title': forms.TextInput(attrs={
            'class': 'title',
            'placeholder': 'Write the title of your post.'}),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write the content of your post.'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add a comment...'}),
        }