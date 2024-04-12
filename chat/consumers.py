import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.manager.consumer_manager import ConsumerManager
from chat.models.channel_entity import ChannelEntity
from chat.models.message_entity import MessageEntity
from chat.serializers.message_serialiers import MessageSerializers
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        super(ChatConsumer, self).__init__()
        self.consumer_manager = ConsumerManager()

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        messages = await database_sync_to_async(
            self.get_old_messages)()
        async for message in messages:
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message.message,
                'creation_time': message.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
            }))

    def get_old_messages(self):
        return MessageEntity.objects.filter(channel__channel_name=self.room_name)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )
        user = await database_sync_to_async(self.get_user)(user_id=text_data_json['user_id'])
        channel_obj = await database_sync_to_async(self.get_channel_obj)()
        await database_sync_to_async(self.store_message_in_db)(message, user, channel_obj)
        await self.send_notif(user=user, message=message)

    async def send_notif(self, user, message):
        members = await database_sync_to_async(self.get_member_of_channel)(user_id=user.id)
        await self.channel_layer.group_send(
            'chat_listener', {
                "type": "chat.message",
                "message": message,
                'sender_id': user.id,
                'members': list(members),
                'channel_name': self.room_name,
            }
        )

    @staticmethod
    def store_message_in_db(message, user, channel):
        MessageEntity.objects.create(author=user, message=message, channel=channel)

    @staticmethod
    def get_user(user_id):
        return User.objects.filter(id=user_id).first()

    def get_member_of_channel(self, user_id):
        return list(ChannelEntity.objects.filter(channel_name=self.room_name).first().users.all().exclude(
            id=user_id).values_list('id', flat=True))

    def get_channel_obj(self):
        return ChannelEntity.objects.filter(channel_name=self.room_name).first()

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
