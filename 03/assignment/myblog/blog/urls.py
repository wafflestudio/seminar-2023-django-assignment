
from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    #path('', views.index, name = "index"),
    path('', TemplateView.as_view(template_name='blog/index.html'), name='index'),
    path('blog/', views.main_page, name='main-page'),
    path('list/', views.page_list, name='page-list'),
    path('write/', views.page_create, name='page-create'),
    path('page/<int:page_id>/', views.page_detail, name='page-detail'),
    path('page/<int:page_id>/edit/', views.page_update, name='page-update'),
    path('page/<int:page_id>/delete/', views.page_delete, name='page-delete'),
    path('page/<int:page_id>/comments/', views.comments_create, name='comments-create'),
    path('page/<int:page_id>/comments/<int:comment_id>/delete/', views.comments_delete, name='comments-delete'),
]
