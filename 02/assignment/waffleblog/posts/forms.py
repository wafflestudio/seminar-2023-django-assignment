from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'writer', 'content']

class DeleteForm(forms.Form):
    value = forms.CharField(max_length=50, required=True)