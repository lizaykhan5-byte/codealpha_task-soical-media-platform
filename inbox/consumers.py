import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.username = self.scope["url_route"]["kwargs"]["username"]
        self.current_user = self.scope["user"]

        if self.current_user.is_anonymous:
            await self.close()
            return

        users = sorted([self.current_user.username, self.username])
        self.room_name = f"chat_{users[0]}_{users[1]}"
        self.room_group_name = self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.set_online(True)
        await self.accept()

    async def disconnect(self, close_code):
        await self.set_online(False)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        event_type = data.get("type")

        if event_type == "typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing_status",
                    "sender": self.current_user.username,
                    "is_typing": data.get("is_typing", False)
                }
            )
            return

        message = data.get("message")

        if not message:
            return

        receiver = await self.get_user(self.username)

        is_blocked = await self.is_blocked(
            self.current_user,
            receiver
        )

        if is_blocked:
            return

        saved_message = await self.save_message(
            sender=self.current_user,
            receiver=receiver,
            body=message
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": saved_message.body,
                "sender": self.current_user.username,
                "created_at": saved_message.created_at.strftime("%I:%M %p")
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def typing_status(self, event):
        await self.send(text_data=json.dumps({
            "type": "typing",
            "sender": event["sender"],
            "is_typing": event["is_typing"]
        }))

    @database_sync_to_async
    def get_user(self, username):
        return User.objects.get(username__iexact=username)

    @database_sync_to_async
    def save_message(self, sender, receiver, body):
        return Message.objects.create(
            sender=sender,
            receiver=receiver,
            body=body
        )

    @database_sync_to_async
    def set_online(self, status):
        profile = self.current_user.profile
        profile.is_online = status
        profile.save()

    @database_sync_to_async
    def is_blocked(self, sender, receiver):
        return (
            receiver in sender.profile.blocked_users.all() or
            sender in receiver.profile.blocked_users.all()
        )