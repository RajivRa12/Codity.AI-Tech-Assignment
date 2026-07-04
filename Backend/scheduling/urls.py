from rest_framework.routers import DefaultRouter
from .views import ScheduleViewSet, ScheduleExecutionViewSet

router = DefaultRouter()
router.register('schedules', ScheduleViewSet)
router.register('schedule-executions', ScheduleExecutionViewSet)

urlpatterns = router.urls
