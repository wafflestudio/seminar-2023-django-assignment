from django.urls import path
from .views import UserRegistrationView, UserDetailView, CustomObtainAuthToken
from rest_framework.authtoken import views

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('token/', views.obtain_auth_token, name='obtain_auth_token'),
]
