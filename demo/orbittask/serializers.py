from rest_framework import serializers
from orbittask.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "args",
            "kwargs",
            "status",
            "result",
            "error",
            "retries",
            "max_retries",
            "eta",
            "created_at",
            "started_at",
            "finished_at"
        ]
        read_only_fields = [
            "id",
        ]