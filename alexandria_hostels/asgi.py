# alexandria_hostels/asgi.py
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from main import routing as main_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alexandria_hostels.settings')
django.setup()

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            main_routing.websocket_urlpatterns
        )
    ),
})