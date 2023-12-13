from django.urls import path


import chat.views

urlpatterns = [
    path('character/', chat.views.getcharacter, name='character'),
    path('chats/', chat.views.chatmanager, name='chats'),
    path('chats/delete-all/', chat.views.chatdestroyer, name='delete-all'),
]
