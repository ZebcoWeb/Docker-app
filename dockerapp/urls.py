from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from app import urls as app_urls


schema_view = get_schema_view(
   openapi.Info(
      title="Apps API",
      default_version='v1',
   )
)


urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),

    path("admin/", admin.site.urls),
    path('apps/', include(app_urls)),
]
