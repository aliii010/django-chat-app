from django.contrib.auth.models import User
from django.db import models


class GroupChat(models.Model):  
  name = models.CharField(max_length=255, unique=True)
  users = models.ManyToManyField(User, related_name='group_chats')

  def __str__(self):
    return self.name
    

class Message(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='messages', null=True)
  content = models.TextField()
  group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='messages', null=True)

  def __str__(self):
    return f'{self.user.username}: {self.content[:20]}...'
