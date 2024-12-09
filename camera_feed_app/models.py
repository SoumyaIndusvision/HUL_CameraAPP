from django.db import models

class Cluster(models.Model):
    name = models.CharField(max_length=255)  # Name of the cluster

    def __str__(self):
        return self.name

class Camera(models.Model):
    name = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=15)  # IP address of the camera
    port = models.IntegerField(default=554)       # RTSP default port
    username = models.CharField(max_length=255)   # Login username for camera
    password = models.CharField(max_length=255)   # Login password for camera
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE, related_name='cameras')  # Association with Cluster

    def __str__(self):
        return self.name