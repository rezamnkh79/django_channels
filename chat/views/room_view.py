from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from chat.models.channel_entity import ChannelEntity


class RoomView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self):
        super(RoomView, self).__init__()

    def get(self, request, room_name):
        if ChannelEntity.objects.filter(channel_name=room_name).first() is None:
            channel_obj = ChannelEntity.objects.create(channel_name=room_name)
            channel_obj.users.add(request.user)

        else:
            channel_obj = ChannelEntity.objects.get(channel_name=room_name)
            if channel_obj.users.filter(id=request.user.id).first() is None:
                channel_obj.users.add(request.user)
        return render(request, "chat/room.html", {"room_name": room_name, 'user': request.user})
