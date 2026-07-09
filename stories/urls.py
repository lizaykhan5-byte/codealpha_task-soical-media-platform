from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_story, name="create_story"),
    path("<int:story_id>/", views.story_detail, name="story_detail"),
    path("delete/<int:story_id>/", views.delete_story, name="delete_story"),
]