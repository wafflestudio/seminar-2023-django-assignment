from django.urls import path
from . import views

urlpatterns=[
   path('signup/', views.SignUpView.as_view(), name='signup'),
   path('login/', views.LoginView.as_view(), name='login'),

   path('posts/', views.PostList.as_view(), name='posts_base'),
   path('posts/tag/<str:tag_name>/', views.PostListByTag.as_view(), name='post<-tag'),
   path('posts/detail/<int:pk>/', views.PostDetail.as_view(), name='posts_detail'),
   
   path('comments/', views.CommentList.as_view(), name='comment_base'),
   path('comments/post/<int:post_id>/', views.CommentListByPost.as_view(), name='comments<-post'),
   path('comments/tag/<str:tag_name>/', views.CommentListByTag.as_view(), name='comments<-tag'),
   path('comments/detail/<int:pk>/', views.CommentDetail.as_view(), name='comment_detail'),
]