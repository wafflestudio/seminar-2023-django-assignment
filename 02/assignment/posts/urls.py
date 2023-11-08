from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name='index'),
    path("posts/", views.gomainpage, name='post-bin'),
    path("posts/<int:post_id>/", views.detailView, name='post-detail'),
    path("posts/new/", views.createView, name='post-create'),
    path("posts/<int:post_id>/update/", views.updateView, name='post-update'),
    path("posts/<int:post_id>/delete/", views.deleteView, name='post-delete'),
    path("posts/<int:post_id>/comments/<int:comment_id>/delete", views.commentDelete, name='comment-delete'),
    path("posts/<int:post_id>/comments/<int:comment_id>/update", views.commentUpdate, name='comment-update')
]