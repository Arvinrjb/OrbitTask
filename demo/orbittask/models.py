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
