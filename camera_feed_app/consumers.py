# import cv2
# import base64
# import logging
# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# from asgiref.sync import sync_to_async
# from .models import Camera
# import asyncio

# logger = logging.getLogger(__name__)

# # Shared Camera Stream Manager
# class CameraStreamManager:
#     def __init__(self, camera_url):
#         self.camera_url = camera_url
#         self.capture = cv2.VideoCapture(camera_url)
#         if not self.capture.isOpened():
#             logger.error(f"Failed to open stream for {camera_url}")
#         else:
#             logger.info(f"Stream opened for {camera_url}")
#         self.is_running = self.capture.isOpened()

#     def read_frame(self):
#         if self.is_running:
#             ret, frame = self.capture.read()
#             if ret:
#                 _, jpeg_frame = cv2.imencode('.jpg', frame)
#                 logger.info(f"Frame successfully encoded for {self.camera_url}")
#                 return base64.b64encode(jpeg_frame).decode('utf-8')
#             else:
#                 logger.error(f"Failed to capture frame for {self.camera_url}")
#         return None

#     def stop(self):
#         if self.capture.isOpened():
#             self.capture.release()
#         self.is_running = False
#         logger.info(f"Stream stopped for {self.camera_url}")


# # Shared camera streams
# shared_camera_streams = {}

# class CameraStreamConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.camera_id = self.scope['url_route']['kwargs']['camera_id']
#         logger.info(f"Attempting to connect to Camera ID {self.camera_id}")

#         try:
#             # Fetch camera details from the database
#             camera = await self.get_camera_by_id(self.camera_id)
#             camera_url = f"rtsp://{camera.username}:{camera.password}@{camera.ip_address}:{camera.port}/cam/realmonitor?channel=1&subtype=0"

#             # Initialize or reuse the shared camera stream
#             if camera_url not in shared_camera_streams:
#                 shared_camera_streams[camera_url] = CameraStreamManager(camera_url)
#             self.camera_stream = shared_camera_streams[camera_url]

#             if not self.camera_stream.is_running:
#                 logger.error(f"Unable to open camera stream for Camera ID {self.camera_id}.")
#                 await self.close()

#             await self.accept()
#             logger.info(f"Connection accepted for Camera ID {self.camera_id}")

#             # Start sending frames to the frontend
#             await self.send_frames()

#         except Exception as e:
#             logger.error(f"Error connecting to Camera {self.camera_id}: {str(e)}")
#             await self.send(text_data=json.dumps({"error": "Unable to connect to camera feed."}))
#             await self.close()

#     async def send_frames(self):
#         try:
#             while True:
#                 frame_data = self.camera_stream.read_frame()
#                 if not frame_data:
#                     logger.error(f"Failed to fetch frame for Camera ID {self.camera_id}.")
#                     break
#                 await self.send(text_data=json.dumps({"frame": frame_data}))
#                 await asyncio.sleep(0.05)  # Control the frame rate to avoid high CPU usage
#         except Exception as e:
#             logger.error(f"Error during frame transmission: {str(e)}")
#         finally:
#             logger.info(f"Closing connection for Camera ID {self.camera_id}")
#             await self.close()

#     async def disconnect(self, close_code):
#         logger.info(f"Disconnected from Camera {self.camera_id}")
#         # If no clients are connected to this camera, stop the stream
#         camera_url = self.camera_stream.camera_url
#         if camera_url in shared_camera_streams and not self.camera_stream.is_running:
#             self.camera_stream.stop()
#             del shared_camera_streams[camera_url]

#     @sync_to_async
#     def get_camera_by_id(self, camera_id):
#         """
#         Fetch the camera instance from the database by its ID.
#         """
#         return Camera.objects.get(pk=camera_id)



#############################################################################################################################################

# import cv2
# import base64
# # import asyncio
# import logging
# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# from asgiref.sync import sync_to_async
# from .models import Camera


# logger = logging.getLogger(__name__)

# class CameraStreamConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.camera_id = self.scope['url_route']['kwargs']['camera_id']

#         # Fetch camera details (username, password, IP, etc.) from your database
#         try:
#             camera = await self.get_camera_by_id(self.camera_id)
#             camera_url = f"rtsp://{camera.username}:{camera.password}@{camera.ip_address}:{camera.port}/cam/realmonitor?channel=1&subtype=0"

#             self.capture = cv2.VideoCapture(camera_url)
#             if not self.capture.isOpened():
#                 logger.error("Unable to open camera stream.")
#                 await self.close()

#             await self.accept()

#             # Start sending frames to frontend
#             await self.send_frames()

#         except Exception as e:
#             logger.error(f"Error while connecting to camera {self.camera_id}: {str(e)}")
#             await self.send(text_data="Error: Unable to connect to camera feed.")
#             await self.close()

#     async def send_frames(self):
#         while True:
#             ret, frame = self.capture.read()
#             if not ret:
#                 logger.error("Failed to read frame from camera")
#                 await self.close()

#             # Encode the frame as JPEG
#             ret, jpeg_frame = cv2.imencode('.jpg', frame)
#             if not ret:
#                 logger.error("Failed to encode frame")
#                 await self.close()

#             # Convert JPEG to base64
#             frame_data = base64.b64encode(jpeg_frame).decode('utf-8')

#             # Send the frame as a WebSocket message
#             await self.send(text_data=json.dumps({"frame": frame_data}))

#             # Add delay to avoid high CPU usage
#             # await asyncio.sleep(0.1)

#     async def disconnect(self, close_code):
#         if hasattr(self, 'capture') and self.capture.isOpened():
#             self.capture.release()
#         logger.info(f"Disconnected from camera {self.camera_id}")

#     @sync_to_async
#     def get_camera_by_id(self, camera_id):
#         """
#         Fetch the camera instance from the database by its ID.
#         """
#         return Camera.objects.get(pk=camera_id)

#############################################################################################################################################


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
