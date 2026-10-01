from django.urls import path

from .views import (
    PostListCreateView,
    PostCommentListCreateView,
    health,
    readiness,
)


urlpatterns = [
    path(
        "posts/",
        PostListCreateView.as_view(),
        name="posts",
    ),
    path(
        "posts/<int:post_id>/comments/",
        PostCommentListCreateView.as_view(),
        name="post-comments",
    ),
    path(
        "health/",
        health,
        name="health",
    ),
    path(
        "readiness/",
        readiness,
        name="readiness",
    ),
]
