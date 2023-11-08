from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index),
    path("posts/", views.posts_list, name="posts_list"),
    path('posts/create', views.post_create, name="post_create"),
    path("posts/<int:post_id>", views.post_detail, name="post_detail"),
    path('posts/<int:post_id>/edit', views.post_update, name="post_update"),
    path('posts/<int:post_id>/delete', views.post_delete, name="post_delete"),
]
