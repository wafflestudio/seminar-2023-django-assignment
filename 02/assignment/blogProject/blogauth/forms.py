from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# 현재 활성화된 사용자 모델을 가져옵니다.
User = get_user_model()

# CustomUserCreationForm 클래스 정의
class CustomUserCreationForm(UserCreationForm):
   class Meta(UserCreationForm.Meta):
      model = User  # User 모델을 커스텀 모델로 설정
      fields = UserCreationForm.Meta.fields
