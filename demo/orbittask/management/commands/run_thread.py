import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from redis.exceptions import TimeoutError as RedisTimeoutError
from concurrent.futures import ThreadPoolExecutor
from orbittask.models import Task, Logs
from orbittask.conf import get_redis
from orbittask.registry import TASK_registery_thread


# get object from database and get functions from TASK_registery 
def get_task(id):
    try:
        obj = Task.objects.get(id=id)
        func = TASK_registery_thread.get(obj.registry)
        return obj, func
    except Task.DoesNotExist:
        raise Exception("Error while get Task")

# run task function
def run_task(task_id):
    task, func = get_task(task_id)
    Logs.objects.create(
        task=task,
        detail="Task Running",
        level="INFO"
    )
    task.status = "RUNNING"
    task.started_at = timezone.now()
    task.save(
        update_fields=[
            "status",
            "started_at"
        ]
    )

    result = None
    for _ in range(task.max_retries):
        try:
            result = func(*task.args, **task.kwargs)
            break
        except:
            task.retries+=1
            continue
    finish_time = timezone.now()
    task.finished_at = finish_time

    if result is None:
        Logs.objects.create(
            task=task,
            detail="The task did not execute successfully.",
            level="ERROR",
            finished_at=finish_time
        )
        task.status = "FAILED"
        task.error = f"Error, task: {task.name}"
        task.save(
            update_fields=[
                "status",
                "error",
                "retries",
                "started_at",
                "finished_at",
            ]
        )
    else:
        Logs.objects.create(
            task=task,
            detail="The task executed successfully.",
            level="INFO",
            finished_at=finish_time
        )
        task.status = "SUCCESS"

    task.result = str(result)
    task.save(
        update_fields=[
            "status",
            "retries",
            "result",
            "started_at",
            "finished_at"
        ]
    )


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--workers",
            type=int,
            default=2
        )

    def handle(self, *args, **options):
        workers=options["workers"]
        redis = get_redis()
        self.stdout.write("Worker started. Waiting for tasks...")
        self.stdout.write(f"Registered tasks: {list(TASK_registery_thread.keys())}")
        # for I/O bound tasks
        with ThreadPoolExecutor(max_workers=workers) as executor:
            while True:
                try:
                    task_redis = redis.brpop("orbittask:queue:thread", timeout=5)
                except RedisTimeoutError:
                    continue

                if task_redis is None:
                    continue
                
                message = json.loads(task_redis[1])
                task_id = message["id"]
                executor.submit(run_task, task_id)
               