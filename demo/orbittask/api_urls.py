from rest_framework.routers import DefaultRouter
from orbittask.views import AddTaskViewSet, ViewTaskViewSet

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

urlpatterns = router.urls