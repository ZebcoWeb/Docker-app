
import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from realtime.consumers import InstanceConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dockerapp.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": 
            URLRouter(
            [
                path("instance", InstanceConsumer.as_asgi()),
        ]
    ),
})
