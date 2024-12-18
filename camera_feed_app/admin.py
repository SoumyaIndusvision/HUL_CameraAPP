from django.contrib import admin
from .models import Cluster, Machine, Camera

@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Display cluster ID and name in the admin list view
    search_fields = ('name',)  # Enable searching by cluster name
    ordering = ('name',)  # Order clusters by name in ascending order

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cluster')  # Display machine ID, name, and associated cluster
    search_fields = ('name', 'cluster__name')  # Enable searching by machine name or cluster name
    list_filter = ('cluster',)  # Add filter for clusters
    ordering = ('id',)  # Order machines by id in ascending order

@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ip_address', 'port', 'get_machine_name', 'get_cluster_name')
    ordering = ('id',)
    
    def get_machine_name(self, obj):
        return obj.machine.name
    
    get_machine_name.short_description = "Machine Name"

    def get_cluster_name(self, obj):
        return obj.machine.cluster.name
    
    get_cluster_name.short_description = "Cluster Name"

