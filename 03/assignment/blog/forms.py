from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):
    TagPost = forms.CharField(max_length=100, required=False, help_text="쉼표(,)로 구분해서 띄어쓰기 없이 입력")
    class Meta:
        model = Post
        fields = ['title', 'description', 'TagPost']

class CommentForm(forms.ModelForm):
    TagComment = forms.CharField(max_length=100, required=False, help_text="쉼표(,)로 구분해서 띄어쓰기 없이 입력")
    class Meta:
        model = Comment
        fields = ['content', 'TagComment']