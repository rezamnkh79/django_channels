from rest_framework import serializers

from chat.models.message_entity import MessageEntity
from django.contrib.auth.models import User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')


class MessageSerializers(serializers.ModelSerializer):
    author = UsersSerializer(many=True, read_only=True)

    class Meta:
        model = MessageEntity
        fields = ['author', 'message', 'creation_time']
