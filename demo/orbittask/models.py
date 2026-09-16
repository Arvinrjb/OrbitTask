from django.db import models


class Task(models.Model):
    class Statuses(models.TextChoices):
        PENDING = "PENDING"
        RUNNING = "RUNNING"
        SUCCESS = "SUCCESS"
        FAILED = "FAILED"
        RETRYING = "RETRYING"

    name = models.CharField(
        max_length=256,
    )
    registry = models.CharField(
        max_length=256,
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
    repeat = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )
    max_repeat = models.IntegerField(
        null=False,
        blank=False,
        default=1
    )
    result = models.TextField(
        max_length=512,
        null=True,
        blank=True,
    )
    error = models.TextField(
        max_length=256,
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
        related_name="logs",
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
        default=Level.INFO,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
