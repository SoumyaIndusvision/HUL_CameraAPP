from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Cluster, Machine, Camera
from .serializers import (
    ClusterSerializer,
    MachineSerializer,
    CameraSerializer,
    CameraStreamSerializer
)
from .streaming import stream_camera_feed


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
    
    

class CameraStreamView(viewsets.ViewSet):
    """ViewSet for streaming camera feeds"""

    @swagger_auto_schema(
        operation_description="For Streaming the Camera Feed by the Camera ID.",
        # responses={200: CameraStreamSerializer}
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
