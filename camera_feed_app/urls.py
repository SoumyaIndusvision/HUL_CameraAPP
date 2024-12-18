from rest_framework.routers import DefaultRouter
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

urlpatterns = router.urls
