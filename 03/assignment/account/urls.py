from django.urls import path
from .views import login_view,logout_view, signup_view

urlpatterns = [
    path("login/", login_view, name='login-page'),
    path("logout/", logout_view, name='logout-page'),
    path("signup/", signup_view, name='signup-page'),
]