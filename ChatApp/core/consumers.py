import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import Group as AuthGroup
from .models import Message, Doubt
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.room_group_name = f'group_{self.group_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        sender_username = data.get('sender')
        msg_type = data.get('type', 'chat')  # 'chat', 'doubt', 'pdf'

        if msg_type == 'chat':
            await self.save_message(sender_username, message)
        elif msg_type == 'doubt':
            # Save doubt or notify - custom implementation if needed
            pass

        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username,
                'msg_type': msg_type,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, username, content):
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(username=username)
            group = AuthGroup.objects.get(id=self.group_id)
            Message.objects.create(sender=user, group=group, content=content)
        except Exception:
            pass
