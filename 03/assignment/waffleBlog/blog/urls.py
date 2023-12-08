from django.urls import path
from .views import (PostListCreateView,
                    PostDetailView,
                    CommentListCreateView,
                    CommentDetailView,
                    TagListCreateView,
                    TaggedPostListAPIView,
                    TaggedCommentListAPIView
                    )

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('comments/posts/<int:post_id>/', CommentListCreateView.as_view(), name='comment-list-for-post'),
    path('tags/', TagListCreateView.as_view(), name='tag-list'),
    path('posts/<str:content>/', TaggedPostListAPIView.as_view(), name='tagged_posts'),
    path('comments/<str:content>/', TaggedCommentListAPIView.as_view(), name='tagged_comments'),
]
