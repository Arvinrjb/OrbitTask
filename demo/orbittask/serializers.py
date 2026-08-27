from rest_framework import serializers
from orbittask.models import Task, Logs


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "registry",
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
            "status",
            "result",
            "retries",
            "error",
            "created_at",
            "started_at",
            "finished_at"
        ]

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = [
            "detail",
            "level",
            "created_at",
            "finished_at"
        ]