from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {'title': forms.TextInput(attrs={
            'class': 'title',
            'placeholder': '제목을 입력 하세요.'}),
            'content': forms.Textarea(attrs={
                'placeholder': '내용을 입력하세요.'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': '댓글을 작성해주세요.'}),
        }