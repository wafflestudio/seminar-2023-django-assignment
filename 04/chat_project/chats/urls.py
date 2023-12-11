from django.urls import path
from .views import CharacterInfoAPI

urlpatterns = [
    path('character/', CharacterInfoAPI.as_view()),
]
