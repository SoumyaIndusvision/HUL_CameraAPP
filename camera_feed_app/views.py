from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Cluster, Machine, Camera
from .serializers import (
    ClusterSerializer, ClusterDetailSerializer,
    MachineSerializer, MachineDetailSerializer,
    CameraSerializer, CameraDetailSerializer,
    CameraStreamSerializer
)
from .streaming import stream_camera_feed


class ClusterViewSet(viewsets.ViewSet):
    """ViewSet for managing clusters"""

    def list(self, request):
        clusters = Cluster.objects.all()
        serializer = ClusterSerializer(clusters, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ClusterSerializer)
    def create(self, request):
        serializer = ClusterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            cluster = Cluster.objects.get(pk=pk)
            serializer = ClusterDetailSerializer(cluster)
            return Response(serializer.data)
        except Cluster.DoesNotExist:
            return Response({"error": "Cluster not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def retrieve_machines(self, request, pk=None):
        try:
            cluster = Cluster.objects.get(pk=pk)
            machines = cluster.machines.all()
            serializer = MachineSerializer(machines, many=True)
            return Response(serializer.data)
        except Cluster.DoesNotExist:
            return Response({"error": "Cluster not found"}, status=status.HTTP_404_NOT_FOUND)


class MachineViewSet(viewsets.ViewSet):
    """ViewSet for managing machines"""

    def list(self, request):
        machines = Machine.objects.all()
        serializer = MachineSerializer(machines, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            machine = Machine.objects.get(pk=pk)
            serializer = MachineDetailSerializer(machine)
            return Response(serializer.data)
        except Machine.DoesNotExist:
            return Response({"error": "Machine not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=MachineSerializer)
    def create(self, request):
        serializer = MachineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve_cameras(self, request, pk=None):
        try:
            machine = Machine.objects.get(pk=pk)
            cameras = machine.cameras.all()
            serializer = CameraSerializer(cameras, many=True)
            return Response(serializer.data)
        except Machine.DoesNotExist:
            return Response({"error": "Machine not found"}, status=status.HTTP_404_NOT_FOUND)


class CameraViewSet(viewsets.ViewSet):
    """ViewSet for managing cameras"""

    def list(self, request):
        cameras = Camera.objects.all()
        serializer = CameraSerializer(cameras, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            camera = Camera.objects.get(pk=pk)
            serializer = CameraDetailSerializer(camera)
            return Response(serializer.data)
        except Camera.DoesNotExist:
            return Response({"error": "Camera not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=CameraSerializer)
    def create(self, request):
        serializer = CameraSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CameraStreamView(viewsets.ViewSet):
    """ViewSet for streaming camera feeds"""

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'camera_id', openapi.IN_PATH,
                description="ID of the camera to stream",
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def retrieve(self, request, pk=None):
        try:
            camera = Camera.objects.get(pk=pk)
            # Simulate streaming logic from the streaming module
            stream_data = stream_camera_feed(camera)
            serializer = CameraStreamSerializer(data=stream_data)
            if serializer.is_valid():
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Camera.DoesNotExist:
            return Response({"status": "inactive", "message": "Camera not found"}, status=status.HTTP_404_NOT_FOUND)
