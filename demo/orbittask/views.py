from rest_framework import mixins, viewsets
from orbittask.serializers import TaskSerializer
from orbittask.conf import get_permission_classes, get_redis
from orbittask.models import Task


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
        redis.lpush("orbittask:queue", str(serializer.validated_data["id"]))
        serializer.save()