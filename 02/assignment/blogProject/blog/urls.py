from django.contrib import admin
from django.urls import path
from blog.views import PostCreateView, PostDetailView, PostListView, PostDeleteView, PostUpdateView, CommentDeleteView, CommentUpdateView

urlpatterns = [
   path('posts/create/', PostCreateView.as_view(), name="post_create"),
   path('posts/<int:pk>/', PostDetailView.as_view(), name="post_detail"),
   path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
   path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
   path('posts/<int:pk>/comment_delete/', CommentDeleteView.as_view(), name='comment_delete'),
   path('posts/<int:pk>/comment_update/', CommentUpdateView.as_view(), name='comment_update'),
   path('posts/', PostListView.as_view(), name="post_list"),
]