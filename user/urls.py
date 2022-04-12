from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views


app_name = "user"

urlpatterns = [
    path("profile/", user_views.user_profile, name="user-profile"),
    path("register/", user_views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="user/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="user/logout.html"),
        name="logout",
    ),
    path("update/", user_views.update_profile, name="update-profile"),
    path("delete/", user_views.delete_user, name="delete-user"),
]
