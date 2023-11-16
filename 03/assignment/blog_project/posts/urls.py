from django.urls import path

from .views import PostList, PostDetail, CommentList

urlpatterns=[
        path('', PostList.as_view(), name='post-list'),
        path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
        path('posts/<int:pk>/comments', CommentList.as_view()),
]