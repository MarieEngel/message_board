from django.urls import path
from . import views as post_views
from post.views import AddCommentView 
app_name = "post"

urlpatterns = [
    path("<int:id>/", post_views.post, name="post"),
    path("add/", post_views.add_post, name="add-post"),
    path("<int:id>/delete/", post_views.delete_post, name="delete-post"),
    path("<int:id>/update/", post_views.update_post, name="update-post"),
    path("<int:pk>/comment/",AddCommentView.as_view(), name="add_comment"),
    #path("<int:id>/comment/", post_views.add_comment, name="add-comment"),
]
