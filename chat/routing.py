from django.conf.urls import url
from django.urls import re_path, path
from . import consumers, views

websocket_urlpatterns = [
    re_path(r"ws/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/", consumers.SideBarConsumer.as_asgi()),
]
