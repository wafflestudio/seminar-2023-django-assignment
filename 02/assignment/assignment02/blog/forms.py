from django import forms
from django.core.exceptions import ValidationError
from .models import User, Post, Comment


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["nickname"]

    
    def signup(self, request, user):
        user.nickname = self.cleaned_data["nickname"]
        user.save()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
    
    def clean_title(self):
        title = self.cleaned_data.get("title", False)
        if not isinstance(title, str) or len(title) == 0:
            self.add_error("title", ValidationError("Title must contain at least one character"))
        return title

    def clean_content(self):
        content = self.cleaned_data.get("content", False)
        if not isinstance(content, str) or len(content) == 0:
            self.add_error("content", ValidationError("Content must contain at least one character"))
        return content


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        
    
    
    def clean_content(self):
        content = self.cleaned_data.get("content", False)
        if not isinstance(content, str) or len(content) == 0:
            self.add_error("content", ValidationError("Content must contain at least one character"))
        return content