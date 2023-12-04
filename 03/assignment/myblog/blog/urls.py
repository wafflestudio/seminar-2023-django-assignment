
from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    #path('', views.index, name = "index"),
    path('', TemplateView.as_view(template_name='blog/index.html'), name='index'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('blog/', views.main_page, name='main-page'),
    #path('list/', views.page_list, name='page-list'),
    path('list/', views.PostList.as_view(), name='page-list'),
    path('write/', views.page_create, name='page-create'),
    #path('page/<int:page_id>/', views.page_detail, name='page-detail'),
    path('page/<int:page_id>/', views.PostDetail.as_view(), name='page-detail'),
    path('page/<int:page_id>/edit/', views.page_update, name='page-update'),
    path('page/<int:page_id>/delete/', views.page_delete, name='page-delete'),
    #path('page/<int:page_id>/comments/', views.comment_list, name='comment-list'),
    path('page/<int:page_id>/comments/', views.CommentList.as_view(), name='comment-list'),
    #path('page/<int:page_id>/comments/<int:comment_id>/', views.CommentDetail.as_view()),
    path('page/<int:page_id>/comments/new/', views.comments_create, name='comments-create'),
    path('page/<int:page_id>/comments/<int:comment_id>/delete/', views.comments_delete, name='comments-delete'),

    path('tag/posts/<str:tag_name>/', views.post_tag_list),
    path('tag/comments/<str:tag_name>/', views.comment_tag_list),
]
