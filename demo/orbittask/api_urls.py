from rest_framework.routers import DefaultRouter
from orbittask.views import AddTaskViewSet, ViewTaskViewSet, LogsViewSet

router = DefaultRouter()

router.register(
    "addtask",
    AddTaskViewSet,
    basename="Add Tasks"
)

router.register(
    "viewtask",
    ViewTaskViewSet,
    basename="View Tasks"
)

router.register(
    "logs",
    LogsViewSet,
    basename="View Logs"
)

urlpatterns = router.urls