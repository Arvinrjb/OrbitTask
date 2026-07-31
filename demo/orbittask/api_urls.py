from rest_framework.routers import DefaultRouter
from orbittask.views import TaskViewSet

router = DefaultRouter()

router.register(
    "task",
    TaskViewSet,
    basename="Tasks"
)

urlpatterns = router.urls