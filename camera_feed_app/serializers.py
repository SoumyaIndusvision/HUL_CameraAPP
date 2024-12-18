from rest_framework import serializers
from .models import Cluster, Machine, Camera


class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ['id', 'name']


class MachineSerializer(serializers.ModelSerializer):
    cluster_name = serializers.CharField(source='cluster.name', read_only=True)

    class Meta:
        model = Machine
        fields = ['id', 'name', 'cluster', 'cluster_name']

    def validate_cluster(self, value):
        if not Cluster.objects.filter(pk=value.id).exists():
            raise serializers.ValidationError("Cluster does not exist.")
        return value


class ClusterDetailSerializer(serializers.ModelSerializer):
    machines = serializers.SerializerMethodField()

    class Meta:
        model = Cluster
        fields = ['cluster', 'machines']

    def get_machines(self, obj):
        return MachineSerializer(obj.machines.all(), many=True).data

    def to_representation(self, instance):
        return {
            'cluster': instance.name,
            'machines': self.get_machines(instance)
        }


class CameraSerializer(serializers.ModelSerializer):
    machine_name = serializers.CharField(source='machine.name', read_only=True)
    cluster_name = serializers.CharField(source='machine.cluster.name', read_only=True)

    class Meta:
        model = Camera
        fields = [
            'id', 'name', 'ip_address', 'port', 'username', 'password',
            'machine', 'machine_name', 'cluster_name'
        ]

    def validate_machine(self, value):
        if not Machine.objects.filter(pk=value.id).exists():
            raise serializers.ValidationError("Machine does not exist.")
        return value


class MachineDetailSerializer(serializers.ModelSerializer):
    cameras = serializers.SerializerMethodField()

    class Meta:
        model = Machine
        fields = ['machine', 'cameras']

    def get_cameras(self, obj):
        return CameraSerializer(obj.cameras.all(), many=True).data

    def to_representation(self, instance):
        return {
            'machine': instance.name,
            'cameras': self.get_cameras(instance)
        }


class CameraDetailSerializer(serializers.ModelSerializer):
    machine_name = serializers.CharField(source='machine.name', read_only=True)
    cluster_name = serializers.CharField(source='machine.cluster.name', read_only=True)

    class Meta:
        model = Camera
        fields = [
            'id', 'name', 'ip_address', 'port', 'username', 'password',
            'machine', 'machine_name', 'cluster_name'
        ]


class CameraStreamSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField()
    stream_url = serializers.URLField(allow_blank=True, required=False)
