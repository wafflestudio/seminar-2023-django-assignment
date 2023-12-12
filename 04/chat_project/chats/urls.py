from django.urls import path
from .views import CharacterInfoAPI, ChatListCreateAPI, ChatDestroyAPI

urlpatterns = [
    path('character/', CharacterInfoAPI.as_view(), name='character-info'),
    path('chats/', ChatListCreateAPI.as_view(), name='chat-list'),
    path('chats/delete-all/', ChatDestroyAPI.as_view(), name='chat-delete'),
]
