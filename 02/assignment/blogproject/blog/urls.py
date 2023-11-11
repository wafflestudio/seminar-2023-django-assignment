from django.contrib import admin
from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    #main/posts
    #글 목록 보기. 기본 화면.
    path("", views.post_list, name="post-list"), 
    #main/post-write
    #새 글 작성
    path("write/", views.post_write, name='post-write'),
    #개별 글 보기.
    path('<int:post_id>/', views.post_detail, name='post-detail'),
    #글 삭제하기
    path('<int:post_id>/delete/', views.post_delete, name='post-delete'),
    #댓글달기
    path('<int:post_id>/comment/',views.comment_write, name='comment-write'),
    ######path('posts/<int:post_id>/update', views.post_update, name='post-update'),
    path('<int:post_id>/update/', views.post_update, name='post-update'),
    ]