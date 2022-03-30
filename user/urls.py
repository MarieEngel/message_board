from django.urls import path
from . import views as user_views


app_name = 'user'

urlpatterns = [
    path("profile/", user_views.user_profile, name="user-profile"),


 
]