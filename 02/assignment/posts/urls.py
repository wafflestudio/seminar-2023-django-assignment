from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("posts/<int:post_id>/", views.detailView, name='post-detail'),
    path("posts/new/", views.createView, name='post-create'),
]