from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Define the schema view for Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Camera Stream API",
        default_version='v1',
        description="API documentation for camera streaming and management",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # Allow public access to Swagger UI
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('camera_feed_app.urls')),  # Include your app's URL patterns
    
    # Swagger and ReDoc URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
