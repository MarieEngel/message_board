from django.urls import path
from . import views as post_views

app_name = 'post'

urlpatterns = [
    path('<int:id>/', post_views.post, name='post'),
    path('add/', post_views.add_post, name='add-post'),
    path('<int:id>/delete/', post_views.delete_post, name='delete-post'),
    path('<int:id>/update/', post_views.update_post, name='update-post')
]