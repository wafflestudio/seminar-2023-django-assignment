from django.urls import path
from . import views


urlpatterns = [
    path('character/', views.CharacterView.as_view(), name='character'),
    path('chats/', views.ChatListView.as_view(), name='chats'),
    path('chats/delete-all/', views.DeleteAllView.as_view(), name='delete-all'),
]