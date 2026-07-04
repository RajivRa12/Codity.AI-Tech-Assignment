from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Distributed Job Scheduler API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/queues/', include('queues.urls')),
    path('api/jobs/', include('jobs.urls')),
    path('api/workers/', include('workers.urls')),
    path('api/scheduling/', include('scheduling.urls')),
    path('api/retry/', include('retry.urls')),
    path('api/logs/', include('logs.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
