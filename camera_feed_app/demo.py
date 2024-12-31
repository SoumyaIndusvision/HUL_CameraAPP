# views.py:
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Cluster, Machine, Camera
from .serializers import (
    ClusterSerializer,
    MachineSerializer,
    CameraSerializer,
)


import logging
import cv2
from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response



class ClusterViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing Clusters.
    """

    @swagger_auto_schema(
        operation_summary="List all clusters",
        operation_description="Retrieve a list of all clusters."
    )
    def list(self, request):
        clusters = Cluster.objects.all()
        serializer = ClusterSerializer(clusters, many=True)
        return Response({"results": serializer.data, "status": status.HTTP_200_OK})

    @swagger_auto_schema(
        operation_summary="Retrieve a specific cluster by ID",
        operation_description="Fetch details of a single cluster by its ID.",
        
    )
    def retrieve(self, request, pk=None):
        try:
            cluster = Cluster.objects.get(pk=pk)
            serializer = ClusterSerializer(cluster)
            return Response({"results": serializer.data})
        except Cluster.DoesNotExist:
            return Response({'message': 'Cluster not found', "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Create a new cluster",
        operation_description="Create a new cluster by providing its details in the request body.",
        request_body=ClusterSerializer
    )
    def create(self, request):
        serializer = ClusterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Cluster Created Successfully", "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Update an existing cluster",
        operation_description="Update a cluster's details by providing its ID and the updated data in the request body.",
        
        request_body=ClusterSerializer
    )
    def update(self, request, pk=None):
        try:
            cluster = Cluster.objects.get(pk=pk)
            serializer = ClusterSerializer(cluster, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Cluster Updated Successfully", "status": status.HTTP_200_OK})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Cluster.DoesNotExist:
            return Response({'message': 'Cluster not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Delete a cluster",
        operation_description="Delete a cluster by providing its ID in the URL.",
    )
    def destroy(self, request, pk=None):
        try:
            cluster = Cluster.objects.get(pk=pk)
            cluster.delete()
            return Response({"message": "Cluster deleted successfully", "status": "204"})
        except Cluster.DoesNotExist:
            return Response({'message': 'Cluster not found', "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
    

class MachineViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing Machines.
    """

    @swagger_auto_schema(
        operation_summary="List all machines or filter by cluster ID",
        operation_description="Returns a list of all machines or filters machines based on the provided cluster_id query parameter.",
        manual_parameters=[
            openapi.Parameter(
                'cluster_id', openapi.IN_QUERY, 
                description="Filter machines by cluster ID", 
                type=openapi.TYPE_INTEGER, 
                required=False
            )
        ]
    )
    def list(self, request):
        cluster_id = request.query_params.get('cluster_id')  # Get cluster_id from query params
        if cluster_id:
            machines = Machine.objects.filter(cluster_id=cluster_id)  # Filter by cluster ID
        else:
            machines = Machine.objects.all()  # Fetch all machines if no cluster_id is provided

        serializer = MachineSerializer(machines, many=True)
        return Response({"results": serializer.data, "status": status.HTTP_200_OK})

    @swagger_auto_schema(
        operation_summary="Retrieve a specific machine by ID",
        operation_description="Fetch details of a single machine by its ID.",
    )
    def retrieve(self, request, pk=None):
        try:
            machine = Machine.objects.get(pk=pk)
            serializer = MachineSerializer(machine)
            return Response({"results": serializer.data})
        except Machine.DoesNotExist:
            return Response({'message': 'Machine not found', "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Create a new machine",
        operation_description="Create a new machine by providing its details in the request body.",
        request_body=MachineSerializer
    )
    def create(self, request):
        serializer = MachineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Machine Created Successfully", "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Update an existing machine",
        operation_description="Update a machine's details by providing its ID and the updated data in the request body.",
        request_body=MachineSerializer
    )
    def update(self, request, pk=None):
        try:
            machine = Machine.objects.get(pk=pk)
            serializer = MachineSerializer(machine, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Machine Updated Successfully", "status": status.HTTP_200_OK})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Machine.DoesNotExist:
            return Response({'message': 'Machine not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Delete a machine",
        operation_description="Delete a machine by providing its ID in the URL.",
    )
    def destroy(self, request, pk=None):
        try:
            machine = Machine.objects.get(pk=pk)
            machine.delete()
            return Response({"message": "Machine deleted successfully", "status": "204"})
        except Machine.DoesNotExist:
            return Response({'message': 'Machine not found', "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

class CameraViewSet(viewsets.ViewSet):

    @swagger_auto_schema(
        operation_description="List all cameras for a given machine.",
        responses={200: CameraSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'machine_id', openapi.IN_QUERY, 
                description="Filter machines by cluster ID", 
                type=openapi.TYPE_INTEGER, 
                required=False
            )
        ]
    )
    def list(self, request):
        machine_id = request.query_params.get('machine_id')
        if machine_id:
            cameras = Camera.objects.filter(machine_id=machine_id)
        else:
            cameras = Camera.objects.all()
        serializer = CameraSerializer(cameras, many=True)
        return Response({"results": serializer.data,"status":status.HTTP_200_OK})

    @swagger_auto_schema(
        operation_description="Retrieve a specific camera by ID.",
        responses={200: CameraSerializer}
    )
    def retrieve(self, request, pk=None):
        try:
            camera = Camera.objects.get(pk=pk)
        except Camera.DoesNotExist:
            return Response({"message": "Not found.","status":status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

        serializer = CameraSerializer(camera)
        return Response({"results":serializer.data,"status":status.HTTP_200_OK}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new camera.",
        request_body=CameraSerializer,
        responses={201: CameraSerializer}
    )
    def create(self, request):
        serializer = CameraSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Camera Created Successfully","status":status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update an existing camera.",
        request_body=CameraSerializer,
        responses={200: CameraSerializer}
    )
    def update(self, request, pk=None):
        try:
            camera = Camera.objects.get(pk=pk)
        except Camera.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CameraSerializer(camera, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Camera Updated Successfully","status":status.HTTP_201_CREATED})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a camera.",
        responses={204: 'No content'}
    )
    def destroy(self, request, pk=None):
        try:
            camera = Camera.objects.get(pk=pk)
        except Camera.DoesNotExist:
            return Response({"detail": "Not found.","status":"204"})

        camera.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

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
    """
    Streams the video feed from the camera.
    """
    try:
        # Construct the RTSP URL using the camera's credentials
        camera_url = f"rtsp://{camera.username}:{camera.password}@{camera.ip_address}:{camera.port}/cam/realmonitor?channel=1&subtype=0"
        logger.info(f"Checking camera connection at {camera_url}")
        
        # Check if the camera is active
        if not check_camera_status(camera_url):
            logger.error(f"Unable to connect to the camera feed at {camera_url}")
            return None
        
        # Function to stream the video as MJPEG
        def generate():
            cap = cv2.VideoCapture(camera_url)
            try:
                while True:
                    if not cap.isOpened():
                        logger.warning("Camera feed disconnected. Attempting to reconnect...")
                        cap.release()
                        cap = cv2.VideoCapture(camera_url)
                        continue
                    
                    ret, frame = cap.read()
                    if not ret:
                        logger.warning("Failed to read frame. Reconnecting...")
                        cap.release()
                        cap = cv2.VideoCapture(camera_url)
                        continue
                    
                    _, jpeg = cv2.imencode('.jpg', frame)
                    frame = jpeg.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n'
                           b'Content-Length: ' + str(len(frame)).encode() + b'\r\n\r\n' +
                           frame +
                           b'\r\n')
            except GeneratorExit:
                logger.info("Client disconnected. Closing stream.")
            except Exception as e:
                logger.error(f"Error in stream: {e}")
            finally:
                cap.release()

        return StreamingHttpResponse(
            generate(),
            content_type="multipart/x-mixed-replace; boundary=frame"
        )
    
    except Exception as e:
        logger.error(f"Error while streaming camera feed: {str(e)}")
        return None

class CameraStreamView(APIView):
    """APIView for streaming camera feeds"""
    
    def get(self, request, pk=None):
        try:
            camera = Camera.objects.get(pk=pk)
            stream_response = stream_camera_feed(camera)
            
            if stream_response:
                return stream_response
            else:
                return Response({"status": "inactive", "message": "Unable to connect to the camera feed."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Camera.DoesNotExist:
            return Response({"status": "inactive", "message": "Camera not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return Response({"status": "inactive", "message": f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# settings.py:
"""
Django settings for camera_feed_proj project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
from django.conf import settings
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j4-lxr9r-b6p3o2filh$4!=63d0+tbd!ib257=u8vew&68yrlu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CORS_ALLOW_ALL_ORIGINS = True

CORS_ORIGIN_ALLOW_ALL=True

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'https://cctv.indusvision.in',
    'https://www.cctv.indusvision.in',
]

ALLOWED_HOSTS = ['*','localhost', '127.0.0.1', 'cctv.indusvision.in', 'www.cctv.indusvision.in','cctv.localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'camera_feed_app',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'camera_feed_proj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'camera_feed_proj.wsgi.application'

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,  # Set to False if you're using Token/JWT authentication
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        },
    },
    'PERSIST_AUTH': True,
    'SCHEMA_URL': 'https://hul.aivolved.in/swagger.json'
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": settings.SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}   


AUTH_USER_MODEL = 'users.User'



# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'site', 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'site', 'static', 'build')
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
