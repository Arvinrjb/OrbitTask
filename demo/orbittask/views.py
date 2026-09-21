import json
from django.utils import timezone
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.validated_data
        if task["registry"] in TASK_registery_thread:
            queue = "orbittask:queue:thread"
        elif task["registry"] in TASK_registery_process:
            queue = "orbittask:queue:process"
            return Response(
                "Task not registered",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        instance = self.perform_create(serializer)
        message = {
            "id": str(instance.id),
            "registry": str(instance.registry),
            "eta":instance.eta.isoformat() if instance.eta else None
        }
        redis.lpush(queue, json.dumps(message))

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def get_permissions(self):
        return get_add_permission_classes()
    
    def perform_create(self, serializer):
        return serializer.save()


class ViewTaskViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ViewTaskSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.registry in TASK_registery_thread:
            queue = "orbittask:delayed:thread"
        elif instance.registry in TASK_registery_process:
            queue = "orbittask:delayed:process"

        message = {
            "id": str(instance.id),
            "registry": str(instance.registry),
            "eta":timezone.localtime(instance.eta).isoformat()

        }
        removed = redis.zrem(queue, json.dumps(message))

        print("REMOVED:", removed)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


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