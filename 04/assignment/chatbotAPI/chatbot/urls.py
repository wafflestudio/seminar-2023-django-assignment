from django.urls import path

from .views import CharacterListAPI, ChatListCreateAPI, ChatDeleteAPI

urlpatterns = [
    path('character/', CharacterListAPI.as_view()),
    path('chats/', ChatListCreateAPI.as_view()),
    path('chats/delete-all/', ChatDeleteAPI.as_view()),
]
