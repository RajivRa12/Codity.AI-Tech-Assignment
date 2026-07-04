from rest_framework.routers import DefaultRouter
from .views import WorkerViewSet

router = DefaultRouter()
router.register('workers', WorkerViewSet)

urlpatterns = router.urls
