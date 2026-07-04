from rest_framework.routers import DefaultRouter
from .views import RetryPolicyViewSet, RetryAttemptViewSet

router = DefaultRouter()
router.register('policies', RetryPolicyViewSet)
router.register('attempts', RetryAttemptViewSet)

urlpatterns = router.urls
