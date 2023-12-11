from django.urls import path
from .views import CharacterInfoAPI, ChatListCreateAPI, ChatDestroyAPI

urlpatterns = [
    path('character/', CharacterInfoAPI.as_view()),
    path('chats/', ChatListCreateAPI.as_view()),
    path('chats/delete-all/', ChatDestroyAPI.as_view())
]
