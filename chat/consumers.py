import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import GroupChat, Message
from django.contrib.auth.models import User
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user_id = self.scope["user"].id
        
        user = await database_sync_to_async(User.objects.get)(id=user_id)
        group_chat = await database_sync_to_async(GroupChat.objects.get)(name=self.room_name)  # name is unique
        
        await self.save_message(user, group_chat, message)
        
        """
        'type' key corresponding to the name of the method that should be invoked on consumers.
        This translation is done by replacing . with _, thus in this example, chat.message calls the chat_message method.
        """
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message, "username": user.username}
        )
        
    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "username": username}))

    @database_sync_to_async
    def save_message(self, user, group_chat, message):
        Message.objects.create(user=user, content=message, group_chat=group_chat)
