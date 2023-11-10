from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.main, name="main"), 
    #path("signup/", views.signup, name="main"), 
    #path("signin/", views.signin, name="signin"), 
    path("post/", views.post_list, name="post-list"), 
    path("post/create/", views.post_create, name="post-create"), 
    path("post/<int:post_id>/", views.post_detail, name="post-detail"), 
    path("post/<int:post_id>/update", views.post_update, name="post-update"), 
    path("post/<int:post_id>/delete", views.post_delete, name="post-delete"), 
]
