from django.urls import path
from .views import IndexView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView


urlpatterns = [
    path("", IndexView.as_view(), name="post-index"),
    path("posts/new/", PostCreateView.as_view(), name="post-create"),
    path("posts/<int:post_id>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:post_id>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:post_id>/delete/", PostDeleteView.as_view(), name="post-delete"),
]