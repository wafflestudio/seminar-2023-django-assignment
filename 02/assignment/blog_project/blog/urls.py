from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
     path("", views.MainView.as_view(), name="main"),
     path("posts/<int:post_id>/",
          views.PostDetailView.as_view(),
          name='post-detail'),
     path("posts/new/", views.PostCreateView.as_view(), name="post-create"),
     path("posts/<int:post_id>/edit/",
          views.PostUpdateView.as_view(),
          name="post-update"),
     path("posts/<int:post_id>/delete/",
          views.PostDeleteView.as_view(),
          name="post-delete"),
     path("posts/<int:post_id>/comments/create",
          views.CommentCreateView.as_view(),
          name = 'comment-create')

]