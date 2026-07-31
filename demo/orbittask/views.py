from rest_framework import mixins, viewsets
from orbittask.serializers import TaskSerializer
from orbittask.conf import get_permission_classes
from orbittask.models import Task


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