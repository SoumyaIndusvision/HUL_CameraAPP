import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework import status
from asgiref.sync import sync_to_async
from .views import stream_camera_feed_via_websocket
from .models import Camera

logger = logging.getLogger(__name__)

class CameraStreamWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the camera ID from the WebSocket URL route
        self.camera_id = self.scope['url_route']['kwargs']['camera_id']

        try:
            # Fetch the camera instance
            self.camera = await sync_to_async(Camera.objects.get)(pk=self.camera_id)
        except Camera.DoesNotExist:
            logger.error(f"Camera with ID {self.camera_id} not found.")
            await self.close(code=status.HTTP_404_NOT_FOUND)
            return

        # Accept the WebSocket connection
        await self.accept()

        # Start streaming the camera feed
        await stream_camera_feed_via_websocket(self.camera, self)

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected for camera {self.camera_id}.")
