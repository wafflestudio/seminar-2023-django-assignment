from django.urls import path

import blog.views as views

urlpatterns = [
    path("signup/", views.SignupView.as_view()), 
    path("login/", views.LoginView.as_view()), 
    path("logout/", views.LogoutView.as_view()), 
    path("posts/", views.PostListView.as_view()), 
    path("posts/<int:pk>/", views.PostDetailView.as_view()), 
    path("posts/<int:pk>/comments/", views.PostCommentListView.as_view()),
    path("comments/", views.CommentListView.as_view()), 
    path("comments/<int:pk>/", views.CommentDetailView.as_view()), 
    path("tag/<str:pk>/posts/", views.TagPostListView.as_view()), 
    path("tag/<str:pk>/comments/", views.TagCommentListView.as_view())
]