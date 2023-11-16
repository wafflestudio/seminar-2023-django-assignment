from django.urls import path

from .views import PostListAPI, PostDetailAPI, CommentListAPI, IndexRedirectView

urlpatterns=[
        path('', IndexRedirectView.as_view(), name='index'),
        path('posts/', PostListAPI.as_view(), name='post-list'),
        path('posts/<int:pk>/', PostDetailAPI.as_view(), name='post-detail'),
        path('posts/<int:pk>/comments', CommentListAPI.as_view()),
]