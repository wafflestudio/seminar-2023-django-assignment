from django.urls import path, include
from .views import characterView, chatView, chatDeleteView

urlpatterns = [
    path('character/', characterView.as_view()),
    path('chats/', chatView.as_view()),
    path('chats/delete-all/', chatDeleteView.as_view()),
]
