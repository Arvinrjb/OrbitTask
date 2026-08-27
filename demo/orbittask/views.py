from rest_framework import mixins, viewsets
import json
from orbittask.serializers import TaskSerializer, LogSerializer
from orbittask.conf import get_permission_classes, get_redis
from orbittask.models import Task, Logs
from orbittask.registry import TASK_registery_thread, TASK_registery_process


redis = get_redis()
# API for GET, POST, CREATE, DELETE Tasks
class TaskViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        return Task.objects.all()

    def get_permissions(self):
        return get_permission_classes()

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


# API for View Logs 
class LogsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = LogSerializer

    def get_permissions(self):
        return get_permission_classes()

    def get_queryset(self):
        return Logs.objects.all()