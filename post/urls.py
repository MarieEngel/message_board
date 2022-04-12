from django.urls import path
from . import views as post_views
from post.views import AddCommentView

app_name = "post"

urlpatterns = [
    path("<int:id>/", post_views.post, name="post"),
    path("add/", post_views.add_post, name="add-post"),
    path("<int:id>/delete/", post_views.delete_post, name="delete-post"),
    path("<int:id>/update/", post_views.update_post, name="update-post"),
    path("<int:pk>/comment/", AddCommentView.as_view(), name="add_comment"),
    path("search/", post_views.search, name="search"),
    path(
        "<int:post_id>/comment/<int:pk>/delete/",
        post_views.DeleteCommentView.as_view(),
        name="delete-comment",
    ),
    path(
        "<int:post_id>/comment/<int:pk>/update/",
        post_views.UpdateCommentView.as_view(),
        name="update-comment",
    ),
]
