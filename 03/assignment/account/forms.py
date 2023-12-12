from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

from .models import User

class LoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']

class SignupForm(UserCreationForm):
    nickname = forms.CharField(max_length=30, required=False, help_text="입력하지 않으면 ID로 자동 할당됩니다.")
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'nickname']