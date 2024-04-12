from chat.models.message_entity import MessageEntity
from chat.serializers.message_serialiers import MessageSerializers
from channels.db import database_sync_to_async


class ConsumerManager:
    async def get_user_messages(self, channel_name):
        messages = await database_sync_to_async(MessageEntity.objects.filter)(channel_name=channel_name)
        return messages

    @staticmethod
    def get_message_object(chanel_name):
        return MessageEntity.objects.filter(chanel_name=chanel_name)
