from django.contrib import admin
from .models import Cluster, Camera

# Define the admin class for Cluster
class ClusterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Display these fields in the admin list view
    search_fields = ('name',)     # Enable search functionality by cluster name
    ordering = ('id',)

# Define the admin class for Camera
class CameraAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ip_address', 'port', 'cluster')  # Fields to display in the admin list view
    list_filter = ('cluster',)                                     # Add a filter for clusters in the sidebar
    search_fields = ('name', 'ip_address', 'cluster__name')        # Enable search by name, IP address, and cluster name
    ordering = ('cluster', 'name')                                # Default ordering by cluster and camera name

# Register the models with the admin site
admin.site.register(Cluster, ClusterAdmin)
admin.site.register(Camera, CameraAdmin)
