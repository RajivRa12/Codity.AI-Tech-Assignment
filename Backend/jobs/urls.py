from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, JobExecutionViewSet, ScheduledJobViewSet

router = DefaultRouter()
router.register(r'executions', JobExecutionViewSet, basename='jobexecution')
router.register(r'scheduled', ScheduledJobViewSet, basename='scheduledjob')
router.register(r'', JobViewSet, basename='job')

urlpatterns = [
    path('', include(router.urls)),
]
