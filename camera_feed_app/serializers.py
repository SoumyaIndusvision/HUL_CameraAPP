from rest_framework import serializers
from .models import Cluster, Machine, Camera


class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = '__all__'


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__' 

    
class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'


class CameraStreamSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField()
    stream_url = serializers.URLField(allow_blank=True, required=False)
