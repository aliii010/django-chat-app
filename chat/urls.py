from django.urls import path

from . import views


urlpatterns = [
  path("", views.index, name="index"),
  path("chat/group/<str:room_name>/", views.group_chat, name="chat"),
]