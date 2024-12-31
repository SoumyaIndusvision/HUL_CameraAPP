import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .views import stream_camera_feed  # Import the existing function from views.py
from .models import Camera

logger = logging.getLogger(__name__)

class CameraStreamConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for streaming camera feeds.
    """

    async def connect(self):
        """
        Called when the WebSocket is handshaking as part of the connection process.
        """
        camera_id = self.scope['url_route']['kwargs']['camera_id']
        self.camera_id = camera_id

        # Fetch the camera instance based on its ID
        try:
            self.camera = await sync_to_async(Camera.objects.get)(pk=self.camera_id)
        except Camera.DoesNotExist:
            await self.close()
            return

        # Fetch camera feed using the existing view function
        stream = await sync_to_async(stream_camera_feed)(self.camera)

        # If streaming is successful, start the WebSocket connection
        if stream is not None:
            await self.accept()
            await self.send_camera_feed(stream)
        else:
            await self.send(text_data="Unable to connect to the camera feed.")
            await self.close()

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.
        """
        logger.info(f"Camera feed WebSocket connection closed for camera {self.camera_id}.")

    async def receive(self, text_data):
        """
        Handle incoming WebSocket messages (if any).
        """
        pass  # No messages expected from the client

    async def send_camera_feed(self, stream):
        """
        Continuously send the camera feed through WebSocket.
        """
        # Assuming the stream is a generator like in your original function.
        for frame in stream:
            await self.send(bytes_data=frame)  # Send each frame to WebSocket

