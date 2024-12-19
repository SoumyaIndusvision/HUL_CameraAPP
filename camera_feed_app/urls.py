from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    ClusterViewSet,
    MachineViewSet,
    CameraViewSet,
    CameraStreamView
)

# Create a router to automatically generate URLs for ViewSets
router = DefaultRouter()
router.register(r'clusters', ClusterViewSet, basename='clusters')
router.register(r'machines', MachineViewSet, basename='machines')
router.register(r'cameras', CameraViewSet, basename='cameras')
router.register(r'stream', CameraStreamView, basename='camera_stream')

# Extend urlpatterns to include hierarchical filtering endpoints
urlpatterns = router.urls + [
    path('clusters/<int:pk>/machines/', ClusterViewSet.as_view({'get': 'retrieve_machines'}), name='cluster-machines'),
    path('machines/<int:pk>/cameras/', MachineViewSet.as_view({'get': 'retrieve_cameras'}), name='machine-cameras'),
]
