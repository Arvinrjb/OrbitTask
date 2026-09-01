from rest_framework import mixins, viewsets
import json
from orbittask.serializers import AddTaskSerializer, ViewTaskSerializer, LogSerializer
from orbittask.conf import get_add_permission_classes, get_view_permission_classes, get_redis
from orbittask.models import Task, Logs
from orbittask.registry import TASK_registery_thread, TASK_registery_process


redis = get_redis()
# API for GET, POST, CREATE, DELETE Tasks
class AddTaskViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = AddTaskSerializer

    def get_permissions(self):
        return get_add_permission_classes()

    def perform_create(self, serializer):
        task = serializer.save()
        if task.registry in TASK_registery_thread:
            queue = "orbittask:queue:thread"
        elif task.registry in TASK_registery_process:
            queue = "orbittask:queue:process"
        else:
            task.status = "FAILED"
            task.error = "Task not registered"
            task.save(update_fields=["status", "error"])
            return None
        message = {
            "id": str(task.id),
            "registry": str(task.registry),
        }
        redis.lpush(queue, json.dumps(message))


class ViewTaskViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ViewTaskSerializer

    def get_permissions(self):
        return get_view_permission_classes()

    def get_queryset(self):
        return Task.objects.all()


# API for View Logs 
class LogsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = LogSerializer

    def get_permissions(self):
        return get_view_permission_classes()

    def get_queryset(self):
        return Logs.objects.all()