# chat/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from chat.views.chant_views import ChatView
from chat.views.room_view import RoomView

urlpatterns = [
                  path("", ChatView.as_view(), name="chat"),
                  path("<str:room_name>/", RoomView.as_view(), name="room"),
              ]
