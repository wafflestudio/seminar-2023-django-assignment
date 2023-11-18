from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostListAPI, PostDetailAPI, CommentListAPI, IndexRedirectView, SignUpView, CommentDetailAPI

# router = DefaultRouter()
# router.register('', CommentViewSet, basename='comment')

urlpatterns=[
        path('', IndexRedirectView.as_view(), name='index'),
        path('signup/', SignUpView.as_view(), name='signup'),
        path('posts/', PostListAPI.as_view(), name='post-list'),
        path('posts/<int:pk>/', PostDetailAPI.as_view(), name='post-detail'),
        path('posts/<int:pk>/comments/', CommentListAPI.as_view()),
        path('posts/<int:post_id>/comments/<int:comment_id>/', CommentDetailAPI.as_view()),
        # path('posts/<int:pk>/comments', include(router.urls)),
]