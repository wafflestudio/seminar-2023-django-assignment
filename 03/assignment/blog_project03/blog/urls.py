from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from .views import (
                    PostListView, PostCreateView, PostDetailView,
                    PostUpdateView, PostDeleteView,
                    
                    CommentListView, CommentCreateView,
                    CommentUpdateView, CommentDeleteView,

                    TagListCommentView, TagListPostView,
                    )

urlpatterns = [
     # post
     path('posts', PostListView.as_view(), name='post-list'),
     path('posts/new', PostCreateView.as_view(), name='post-create'),
     path('posts/<int:post_id>', PostDetailView.as_view(), name='post-detail]'),
     path('posts/<int:post_id>/delete', PostDeleteView.as_view(), name='post-delete'),
     path('posts/<int:post_id>/update', PostUpdateView.as_view(), name='post-update'),
     
     # comment
     path('posts/<int:post_id>/comments', CommentListView.as_view(), name='comment-list'),
     path('posts/<int:post_id>/comments/new', CommentCreateView.as_view(), name='comment=create'),
     path('posts/<int:post_id>/comments/<int:comment_id>/update', CommentUpdateView.as_view(), name='comment-update'),
     path('posts/<int:post_id>/comments/<int:comment_id>/delete', CommentDeleteView.as_view(), name='comment-delete'),
     
     # tag
     path('posts/tags/<str:tag_content>', TagListPostView.as_view(), name='tag-post-list'),
     path('comments/tags/<str:tag_content>', TagListCommentView.as_view(), name='tag-comment-list'),
]