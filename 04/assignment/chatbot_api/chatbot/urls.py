from django.urls import path
from . import views


urlpatterns = [
    path('character/', views.character_view),
    path('chats/', views.ChatListCreateAPIView.as_view()),
    path('chats/delete-all/', views.chat_delete_all),
]