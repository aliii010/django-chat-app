from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import GroupChat

def index(request):
  return render(request, "chat/index.html")


def group_chat(request, room_name):
  group_chat, is_created = GroupChat.objects.get_or_create(name=room_name)
  if request.user.is_authenticated:
    group_chat.users.add(request.user)
  
  context = {
    "room_name": room_name,
    "users": group_chat.users.all(),
    "messages": group_chat.messages.all()
  }
  
  return render(request, "chat/group_chat.html", context)
