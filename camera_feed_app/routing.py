from django.urls import re_path
from .consumers import CameraStreamConsumer

websocket_urlpatterns = [
    re_path(r'ws/camera/(?P<camera_id>\d+)/stream/$', CameraStreamConsumer.as_asgi())
]
