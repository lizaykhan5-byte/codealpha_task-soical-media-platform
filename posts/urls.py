from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create-post/", views.create_post, name="create_post"),

    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("post/<int:post_id>/edit/", views.edit_post, name="edit_post"),
    path("post/<int:post_id>/delete/", views.delete_post, name="delete_post"),

    path("like/<int:post_id>/", views.like_post, name="like_post"),
    path("save/<int:post_id>/", views.save_post, name="save_post"),
    path("saved-posts/", views.saved_posts, name="saved_posts"),

    path("comment/<int:post_id>/", views.add_comment, name="add_comment"),
]