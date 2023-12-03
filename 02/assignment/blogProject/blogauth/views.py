from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm

User = get_user_model()

# Create your views here.
class CreateUserView(CreateView): 
   template_name = "blogauth/signup.html"     # signup form 띄우기
   form_class = CustomUserCreationForm
   success_url = reverse_lazy("signup_done") # 회원가입 성공 시 이동할 URL

class RegisteredView(TemplateView): # 회원가입이 완료된 경우
   template_name = "blogauth/signup_done.html"

class CustomLoginView(LoginView):
   template_name = 'blogauth/login.html'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      #context['abc'] = "asdf"
      return context
   
   success_url = reverse_lazy("")