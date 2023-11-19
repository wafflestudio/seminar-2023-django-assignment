from django.urls import path
from .views import IndexView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, CommentCreateView, CommentUpdateView, CommentDeleteView, SearchPostView, SearchCommentView


urlpatterns = [
    #posts
    path("", IndexView.as_view(), name="post-index"),
    path("posts/new/", PostCreateView.as_view(), name="post-create"),
    path("posts/<int:post_id>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:post_id>/update/", PostUpdateView.as_view(), name="post-update"),
    path("posts/<int:post_id>/delete/", PostDeleteView.as_view(), name="post-delete"),

    #comments
    path("posts/<int:post_id>/comment/create", CommentCreateView.as_view(), name="comment-create"),
    path("comment/<int:comment_id>/update", CommentUpdateView.as_view(), name="comment-update"),
    path("comment/<int:comment_id>/delete", CommentDeleteView.as_view(), name="comment-delete"),

    #search
    path("search/posts/", SearchPostView.as_view(), name="search-post"),
    path("search/comments/", SearchCommentView.as_view(), name="search-comment"),
]