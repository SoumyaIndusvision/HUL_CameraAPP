# import logging
# from channels.generic.websocket import AsyncWebsocketConsumer
# from rest_framework import status
# from asgiref.sync import sync_to_async
# from .views import stream_camera_feed_via_websocket
# from .models import Camera

# logger = logging.getLogger(__name__)

# class CameraStreamWebSocketConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Get the camera ID from the WebSocket URL route
#         self.camera_id = self.scope['url_route']['kwargs']['camera_id']

#         try:
#             # Fetch the camera instance
#             self.camera = await sync_to_async(Camera.objects.get)(pk=self.camera_id)
#         except Camera.DoesNotExist:
#             logger.error(f"Camera with ID {self.camera_id} not found.")
#             await self.close(code=status.HTTP_404_NOT_FOUND)
#             return

#         # Accept the WebSocket connection
#         await self.accept()

#         # Start streaming the camera feed
#         await stream_camera_feed_via_websocket(self.camera, self)

#     async def disconnect(self, close_code):
#         logger.info(f"WebSocket disconnected for camera {self.camera_id}.")




import cv2
import base64
import asyncio
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
import json

logger = logging.getLogger(__name__)

class CameraStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.camera_id = self.scope['url_route']['kwargs']['camera_id']

        # Fetch camera details (username, password, IP, etc.) from your database
        try:
            camera = await self.get_camera_by_id(self.camera_id)
            camera_url = f"rtsp://{camera.username}:{camera.password}@{camera.ip_address}:{camera.port}/cam/realmonitor?channel=1&subtype=0"

            self.capture = cv2.VideoCapture(camera_url)
            if not self.capture.isOpened():
                logger.error("Unable to open camera stream.")
                await self.close()

            await self.accept()

            # Start sending frames to frontend
            await self.send_frames()

        except Exception as e:
            logger.error(f"Error while connecting to camera {self.camera_id}: {str(e)}")
            await self.send(text_data="Error: Unable to connect to camera feed.")
            await self.close()

    async def send_frames(self):
        while True:
            ret, frame = self.capture.read()
            if not ret:
                logger.error("Failed to read frame from camera")
                await self.close()

            # Encode the frame as JPEG
            ret, jpeg_frame = cv2.imencode('.jpg', frame)
            if not ret:
                logger.error("Failed to encode frame")
                await self.close()

            # Convert JPEG to base64
            frame_data = base64.b64encode(jpeg_frame).decode('utf-8')

            # Send the frame as a WebSocket message
            await self.send(text_data=json.dumps({"frame": frame_data}))

            # Add delay to avoid high CPU usage
            await asyncio.sleep(0.1)

    async def disconnect(self, close_code):
        if hasattr(self, 'capture') and self.capture.isOpened():
            self.capture.release()
        logger.info(f"Disconnected from camera {self.camera_id}")
