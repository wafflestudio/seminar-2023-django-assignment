from django.contrib import admin
from django.urls import path, include

from blog.views import PostCreateView, PostListView, PostDetailView
from . import views

urlpatterns = [
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/detail/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('posts/', PostListView.as_view(), name='post_list'),
]