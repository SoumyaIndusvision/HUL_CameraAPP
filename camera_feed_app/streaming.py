import cv2
import logging
from django.http import StreamingHttpResponse, JsonResponse

# Set up logging for debugging
logger = logging.getLogger(__name__)

def check_camera_status(camera_url):
    """
    Check if the camera is accessible and return its status.
    """
    cap = cv2.VideoCapture(camera_url)
    if cap.isOpened():
        cap.release()
        return True  # Camera is active
    return False  # Camera is inactive

def stream_camera_feed(camera):
    try:
        # Construct the RTSP URL using the camera's credentials
        camera_url = f"rtsp://{camera.username}:{camera.password}@{camera.ip_address}:{camera.port}/cam/realmonitor?channel=1&subtype=0"
        logger.info(f"Checking camera connection at {camera_url}")
        
        # Check if the camera is active
        if not check_camera_status(camera_url):
            return JsonResponse({"status": "inactive", "message": "Unable to connect to the camera feed."}, status=500)
        
        # Open the camera feed using OpenCV
        cap = cv2.VideoCapture(camera_url)
        if not cap.isOpened():
            logger.error(f"Unable to connect to camera at {camera_url}")
            raise ValueError("Unable to connect to the camera feed.")
        
        # Function to stream the video as MJPEG
        def generate():
            while True:
                ret, frame = cap.read()
                if not ret:
                    logger.warning("Frame not received. Attempting to reconnect.")
                    cap.release()
                    cap.open(camera_url)  # Reconnect
                    continue

                _, jpeg = cv2.imencode('.jpg', frame)
                frame = jpeg.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        
        return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')
    
    except Exception as e:
        logger.error(f"Error while streaming camera feed: {str(e)}")
        return JsonResponse({"status": "inactive", "message": f"Error: {str(e)}"}, status=500)
