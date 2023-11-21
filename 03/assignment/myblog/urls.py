from django.urls import path
from . import views



urlpatterns=[
        #path('', views.IndexRedirectView.as_view(), name='index'),
        path('posts/', views.PostList.as_view(), name='post-list'),
        path('posts/tag/<str:tag_name>/', views.PostListByTag.as_view(), name='post-list-by-tag'),
        #path('posts/new', views.PostCreateView.as_view(), name='post-create'),
        path('posts/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
        #path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
        #path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
        path('signup/', views.SignUpView.as_view(), name='signup'),
        path('login/', views.LoginView.as_view(), name='login'),
        path('comments/', views.CommentList.as_view(), name='comment-list'),
        path('comments/<int:post_id>/', views.CommentList.as_view(), name='comment-list-post'),
        path('comments/detail/<int:pk>/', views.CommentUpdateDelete.as_view(), name='comment-update-delete'),
        path('comments/tag/<str:tag_name>/', views.CommentListByTag.as_view(), name='comment-list-by-tag'),
]