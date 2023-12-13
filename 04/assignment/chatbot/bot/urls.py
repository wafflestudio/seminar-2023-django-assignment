from django.contrib import admin
from django.urls import path, include
from .views import ChatbotDetailView, ChatListCreateView ,ChatDeleteAllView

urlpatterns = [
    # GET: 캐릭터에 대한 정보를 내려줍니다.
    path("character/", ChatbotDetailView.as_view(), name='chatbot-detail'),
    
    # GET: 채팅 목록을 내려줍니다. (character.first_message는 반드시 포함되어야 합니다.)
    # POST: 새로운 채팅을 추가하고, GPT API와 소통해 캐릭터의 새로운 채팅을 만듭니다.
    path("chats/", ChatListCreateView.as_view(), name='chat-list'),

    # POST, DELETE: 지금까지의 전체 채팅을 삭제합니다.
    path("chats/delete-all/", ChatDeleteAllView.as_view(), name='chat-delete'),
]
