from django.urls import path
from . import views

urlpatterns = [
    path("", views.inbox_home, name="inbox"),
    path("chat/<str:username>/", views.chat_room, name="chat_room"),
    path("delete/<str:username>/", views.delete_chat, name="delete_chat"),
    path("block/<str:username>/", views.block_user, name="block_user"),
path("unblock/<str:username>/", views.unblock_user, name="unblock_user"),
]