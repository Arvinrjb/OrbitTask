from rest_framework import serializers
from orbittask.models import Task, Logs


class AddTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "name",
            "registry",
            "args",
            "kwargs",
            "max_retries",
            "eta",
        ]



class ViewTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "args",
            "kwargs",
            "max_retries",
            "status",
            "result",
            "retries",
            "error",
            "eta",
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