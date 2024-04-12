from django.contrib import admin

# Register your models here.
from chat.models.channel_entity import ChannelEntity
from chat.models.message_entity import MessageEntity

admin.site.register(MessageEntity)
admin.site.register(ChannelEntity)
