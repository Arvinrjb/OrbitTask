from django.db import models


class Task(models.Model):
    class Statuses(models.TextChoices):
        PENDING = "PENDING"
        RUNNING = "RUNNING"
        SUCCESS = "SUCCESS"
        FAILED = "FAILED"
        RETRYING = "RETRYING"

    name = models.CharField(
        max_length=20,
    )
    registry = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        default="hello"
    )
    args = models.JSONField(
        default=list,
    )
    kwargs = models.JSONField(
        default=dict,
    )
    status = models.CharField(
        max_length=8,
        choices=Statuses.choices,
        default=Statuses.PENDING,
    )
    result = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )
    error = models.CharField(
        max_length=50,
        default="No Error",
        blank=True,
        null=True,
    )
    retries = models.PositiveSmallIntegerField(
        default=0,
    )
    max_retries = models.PositiveSmallIntegerField(
        default=3,
    )
    eta = models.DateTimeField(
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    started_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    finished_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = [
            "created_at"
        ]


class Logs(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="Tasks",
        null=True,
        blank=True 
    )
    class Level(models.TextChoices):
        INFO = "INFO"
        WARNING = "WARNING"
        ERROR = "ERROR"

    detail = models.TextField(
        max_length=50,
        blank=True,
        null=True
    )
    level = models.CharField(
        max_length=7,
        choices=Level.choices,
        default=Level.INFO
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    finished_at = models.DateTimeField(
        blank=True,
        null=True
    )