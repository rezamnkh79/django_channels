from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from chat.models.channel_entity import ChannelEntity


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self):
        super(ChatView, self).__init__()

    def get(self, request):
        channels = ChannelEntity.objects.filter(users=request.user)
        return render(request, "chat/index.html", context={
            'channels': channels
        })
