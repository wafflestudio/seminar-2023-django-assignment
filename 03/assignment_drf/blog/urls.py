from django.urls import path
from blog import views

urlpatterns = [
    path('', views.PostListCreateAPI.as_view()),
    path('posts/', views.PostListCreateAPI.as_view()),
    path('posts/<int:pk>/', views.PostRetrieveUpdateDestroyAPIView.as_view()),
    path('comments/', views.CommentCreateAPI.as_view()),
    path('comments/<int:pk>/', views.CommentRetrieveUpdateDestroyAPIView.as_view()),
]