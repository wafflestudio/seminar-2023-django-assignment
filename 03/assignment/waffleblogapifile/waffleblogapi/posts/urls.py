from django.urls import path

import posts.views

urlpatterns = [
  path('login/', posts.views.login),
  path('register/', posts.views.register),
  path('posts/', posts.views.post_list),
  path('posts/<str:tag>/', posts.views.post_list_by_tag),
  path('posts/comments/', posts.views.all_comment_list),
  path('posts/comments/<str:tag>/', posts.views.comment_list_by_tag),
  path('posts/<int:pk>/', posts.views.post_detail),
  path('posts/<int:pk>/comments/', posts.views.comment_list),
  path('posts/<int:pk>/comments/<int:comment_pk>/', posts.views.comment_detail),
]