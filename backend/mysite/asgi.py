from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from api.consumers import AudioConsumer   # 新しく作る

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/stream/", AudioConsumer.as_asgi()),
    ]),
     "http": get_asgi_application(),
 })
