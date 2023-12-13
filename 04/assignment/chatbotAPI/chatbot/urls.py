from django.urls import path

from .views import CharacterRetrieveAPI, ChatListCreateAPI, ChatDeleteAPI

urlpatterns = [
    path('character/', CharacterRetrieveAPI.as_view()),
    path('chats/', ChatListCreateAPI.as_view()),
    path('chats/delete-all/', ChatDeleteAPI.as_view()),
]
