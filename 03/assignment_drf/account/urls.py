from django.urls import path
from .views import LoginAPI, SignupAPI

urlpatterns = [
    path('login/', LoginAPI.as_view(), name='login'),
    path('signup/', SignupAPI.as_view(), name='signup'),
]
