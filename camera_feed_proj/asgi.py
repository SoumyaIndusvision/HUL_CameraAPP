import os
import django

# Set the DJANGO_SETTINGS_MODULE before any Django imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'camera_feed_proj.settings')

# Ensure Django is setup before using any Django components
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import camera_feed_app.routing
from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles HTTP requests as usual.
    "websocket": AuthMiddlewareStack(
        URLRouter(
            camera_feed_app.routing.websocket_urlpatterns
        )
    ),
})
