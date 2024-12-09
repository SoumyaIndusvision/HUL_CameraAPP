from django.urls import path
from .views import ClusterNamesListView, ClusterCamerasView, CameraStreamView

urlpatterns = [
    path('clusters/names/', ClusterNamesListView.as_view(), name='cluster_names'),
    path('clusters/<int:cluster_id>/cameras/', ClusterCamerasView.as_view(), name='cluster_cameras'),
    path('camera/<int:camera_id>/stream/', CameraStreamView.as_view(), name='camera_stream'),
]
