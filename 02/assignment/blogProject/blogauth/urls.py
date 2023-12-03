from django.contrib import admin
from django.contrib.auth import views # 로그아웃 기능을 위해 import
from django.urls import path
from .views import CustomLoginView, CreateUserView, RegisteredView

urlpatterns = [
   path('login/', CustomLoginView.as_view(template_name = "blogauth/login.html"), name="login"),
   path('signup/', CreateUserView.as_view(template_name = "blogauth/signup.html"), name="signup"),
   path('signup_done/', RegisteredView.as_view(template_name = "blogauth/signup_done.html"), name="signup_done"),
   path('logout/', views.LogoutView.as_view(), name='logout')
]