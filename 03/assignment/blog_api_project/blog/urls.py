from django.urls import path
from . import views


urlpatterns = [
    path('posts', views.PostListCreateAPIView.as_view(), name='post-list'),
    path('posts/<int:pk>', views.PostRetrieveUpdateDestroyAPIView.as_view()),
    path('posts/<int:pk>/comments', views.CommentListCreateAPIView.as_view()),
    path('comments/<int:pk>', views.CommentUpdateDeleteView.as_view()),
    path('tags/<str:pk>/posts', views.TagPostListView.as_view()),
    path('tags/<str:pk>/comments', views.TagCommentListView.as_view()),
]