from django.urls import path
from .consumers import AudioConsumer

websocket_urlpatterns = [
    path("ws/stream/", AudioConsumer.as_asgi()),
]
