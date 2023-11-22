from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from . import views
from .views import APIPostList, APIPostDetail, APICommentList, APICommentDetail

urlpatterns = [
    path('', views.index, name="index"),
    path('posts/', views.PostListView.as_view(), name='post-list'),
    #path('posts/', views.post_lists, name="post-list"),

    path('posts/new/', views.PostCreateView.as_view(), name='post-create'),
    #path('posts/<int:pk>/', views.post_detail, name="post-detail"),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/<int:editing_comment>/', views.PostDetailView.as_view(), name='post-detail-editcomment'),    
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('posts/tags/<str:tag_name>/', views.post_tag_list, name='post-tag-list'),

    path('tags/', views.tag_search, name='tag-search'),
    
    path('add_comment/<int:pk>/', views.add_comment, name="add_comment"),
    path('edit_comment/<int:pk>/', views.edit_comment, name="edit_comment"),
    path('update_comment/<int:pk>/', views.update_comment, name="update_comment"),
    path('delete_comment/<int:pk>/', views.delete_comment, name="delete_comment"),
    path('comments/tags/<str:tag_name>/', views.comment_tag_list, name='comment-tag-list'),


    path('api/posts', APIPostList.as_view(), name='api-post-list'),
    path('api/posts/<int:pk>', APIPostDetail.as_view(), name='api-post-detail'),
    path('api/posts/<int:pk>/comments', APICommentList.as_view(), name='api-comment-list'),   
    path('api/posts/<int:pk>/comments/<int:comment_pk>', APICommentDetail.as_view(), name='api-comment-detail'),   

    #path('api/token', views.ExampleView.as_view()),
    #path('api-token-auth/', views.ObtainAuthToken.as_view()),
    path('api/login/', views.LoginView.as_view(), name='api-login'),
    path('api/signup/', views.SignupView.as_view(), name='api-signup'),

    path('login/', views.MyLoginView.as_view(), name='login'),
    path('signup/', views.MySignupView.as_view(), name='signup'),

]
