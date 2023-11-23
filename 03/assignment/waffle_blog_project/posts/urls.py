from django.urls import path
from .views import (
    PostListAPIView, 
    PostDetailAPIView, 
    CommentListAPIView, 
    CommentDetailAPIView, 
    PostListByTagAPIView, 
    CommentListByTagAPIView,
    SignUpView,
    )

urlpatterns=[
        path('', PostListAPIView.as_view(), name='post-list'),
        path('signup/', SignUpView.as_view(), name='signup'),
        path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
        path('posts/<int:pk>/comments', CommentListAPIView.as_view()),
        path('posts/<int:post_id>/comments/<int:comment_id>/', CommentDetailAPIView.as_view()),
        path('posts/<str:tags_content>/', PostListByTagAPIView.as_view(), name='post-list-by-tag'),
        path('comments/<str:comment_tags_content>/', CommentListByTagAPIView.as_view(), name='comment-list-by-tag'),

]