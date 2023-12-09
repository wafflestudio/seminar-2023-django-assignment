from django.urls import path
from .views import CharacterListView, ChatListCreateView, ChatDeleteAllView

urlpatterns = [
    path('character/', CharacterListView.as_view(), name='character-list'),
    path('chats/', ChatListCreateView.as_view(), name='chat-list'),
    path('chats/delete-all/', ChatDeleteAllView.as_view(), name='chat-delete-all'),
]