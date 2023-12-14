from django.urls import path
from . import views

urlpatterns = [
    path('character/', views.CharacterList.as_view(), name='character-list'),
    path('chats/', views.ChatListCreateView.as_view(), name='chat-list-create'),
    path('chats/delete-all/', views.ChatListCreateView.as_view(), name='chat-delete-all'),

]
