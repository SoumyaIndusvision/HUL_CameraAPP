from rest_framework import serializers
from .models import Cluster, Camera

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ['id', 'name', 'ip_address', 'port', 'cluster']

class ClusterNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ['id', 'name']

class ClusterSerializer(serializers.ModelSerializer):
    cameras = CameraSerializer(many=True, read_only=True)  # Include cameras in the cluster

    class Meta:
        model = Cluster
        fields = ['id', 'name', 'cameras']
