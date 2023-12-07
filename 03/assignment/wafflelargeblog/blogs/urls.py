from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('', include('dj_rest_auth.urls')),
    path('api/post', views.PostList.as_view()),
    path('api/post/<int:pk>', views.PostDetail.as_view()),
    path('api/post/<int:pk>/comment', views.CommentList.as_view()),
    path('api/comment/<int:pk>', views.CommentDetail.as_view()),
    path('api/tag/<str:tc>/comment', views.TagCommentList.as_view()),
    path('api/tag/<str:tc>/post', views.TagPostList.as_view()),
]
