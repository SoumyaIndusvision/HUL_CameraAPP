"""
ASGI config for camera_feed_proj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import camera_feed_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'camera_feed_proj.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles HTTP requests as usual.
    
    "websocket": AuthMiddlewareStack(
        URLRouter(
            camera_feed_app.routing.websocket_urlpatterns
        )
    ),
})
