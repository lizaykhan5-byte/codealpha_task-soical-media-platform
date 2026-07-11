from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import UserLoginForm
urlpatterns = [

    # Authentication
    path(
        "register/",
        views.register,
        name="register"
    ),
path(
    "login/",
    auth_views.LoginView.as_view(
        template_name="accounts/login.html",
        authentication_form=UserLoginForm
    ),
    name="login"
),
    

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),
    path(
    "password-reset/",
    auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html"
    ),
    name="password_reset",
),

path(
    "password-reset/done/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"
    ),
    name="password_reset_done",
),

path(
    "reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html"
    ),
    name="password_reset_confirm",
),

path(
    "reset/done/",
    auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"
    ),
    name="password_reset_complete",
),
    # Profile
    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    path(
        "profile/edit/",
        views.edit_profile,
        name="edit_profile"
    ),

    # Search
    path(
        "search/",
        views.search_users,
        name="search_users"
    ),

    # Follow Requests
    path(
        "follow-request/<int:request_id>/accept/",
        views.accept_follow_request,
        name="accept_follow_request"
    ),

    path(
        "follow-request/<int:request_id>/reject/",
        views.reject_follow_request,
        name="reject_follow_request"
    ),

    # Followers
    path(
        "user/<str:username>/followers/",
        views.followers_list,
        name="followers_list"
    ),

    # Following
    path(
        "user/<str:username>/following/",
        views.following_list,
        name="following_list"
    ),

    # Follow / Unfollow
    path(
        "user/<str:username>/follow/",
        views.follow_toggle,
        name="follow_toggle"
    ),

    # User Profile (ALWAYS LAST)
    path(
        "user/<str:username>/",
        views.user_profile,
        name="user_profile"
    ),

]
