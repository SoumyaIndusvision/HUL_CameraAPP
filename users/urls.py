from rest_framework.routers import DefaultRouter
from .views import UserAPIView, LoginAPIView, PasswordResetViewSet

router = DefaultRouter()
router.register(r'users', UserAPIView, basename='users')
router.register(r'login', LoginAPIView, basename='login')
router.register(r'password-reset', PasswordResetViewSet, basename='password-reset')

urlpatterns = router.urls