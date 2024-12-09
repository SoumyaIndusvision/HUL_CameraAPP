from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Cluster, Camera
from .serializers import CameraSerializer, ClusterSerializer, ClusterNameSerializer
from .streaming import stream_camera_feed

class ClusterNamesListView(ListAPIView):
    queryset = Cluster.objects.all()
    serializer_class = ClusterNameSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of all clusters (names and IDs only)",
        responses={200: ClusterSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        clusters = self.get_queryset()
        data = [{"id": cluster.id, "name": cluster.name} for cluster in clusters]
        return Response(data, status=status.HTTP_200_OK)

class ClusterCamerasView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve cameras for a specific cluster",
        responses={
            200: CameraSerializer(many=True),
            404: openapi.Response('Cluster not found')
        },
        manual_parameters=[
            openapi.Parameter(
                'cluster_id',
                openapi.IN_PATH,
                description="ID of the cluster to retrieve cameras",
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, request, cluster_id, *args, **kwargs):
        try:
            cluster = Cluster.objects.get(id=cluster_id)
            cameras = cluster.cameras.all()
            serializer = CameraSerializer(cameras, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cluster.DoesNotExist:
            return Response({"error": "Cluster not found"}, status=status.HTTP_404_NOT_FOUND)

class CameraStreamView(APIView):
    @swagger_auto_schema(
        operation_description="Stream a live camera feed by camera ID",
        responses={
            200: openapi.Response('Success'),
            404: openapi.Response('Camera not found'),
            500: openapi.Response('Camera inactive or connection error')
        },
        manual_parameters=[
            openapi.Parameter(
                'camera_id',
                openapi.IN_PATH,
                description="ID of the camera to stream",
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, request, camera_id, *args, **kwargs):
        try:
            camera = Camera.objects.get(id=camera_id)
            return stream_camera_feed(camera)
        except Camera.DoesNotExist:
            return Response({"status": "inactive", "message": "Camera not found"}, status=status.HTTP_404_NOT_FOUND)



