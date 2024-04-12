from django.db import models
from django.contrib.auth import get_user_model

from chat.models.channel_entity import ChannelEntity

user = get_user_model()


class MessageEntity(models.Model):
    channel = models.ForeignKey(ChannelEntity, on_delete=models.CASCADE)
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    message = models.TextField(max_length=2000)
    creation_time = models.DateTimeField(auto_now_add=True)
