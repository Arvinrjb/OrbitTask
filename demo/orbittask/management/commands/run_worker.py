from django.core.management.base import BaseCommand
from django.utils import timezone
from redis.exceptions import TimeoutError as RedisTimeoutError
from concurrent.futures import ThreadPoolExecutor
from orbittask.models import Task
from orbittask.conf import get_redis
from orbittask.registry import TASK_registery


def get_task(id):
    try:
        obj = Task.objects.get(id=id)
        func = TASK_registery.get(obj.name)
        return obj, func
    except Task.DoesNotExist:
        raise Exception("Error while get Task")

def run_task(task_id):
    task, func = get_task(task_id)
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

    task.finished_at = timezone.now()

    if result is None:
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
    def handle(self, *args, **options):
        redis = get_redis()
        self.stdout.write("Worker started. Waiting for tasks...")
        self.stdout.write(f"Registered tasks: {list(TASK_registery.keys())}")
        with ThreadPoolExecutor(max_workers=4) as executor:
            while True:
                try:
                    task_redis = redis.brpop("orbittask:queue", timeout=5)
                except RedisTimeoutError:
                    continue

                if task_redis is None:
                    continue
                
                _, task_id = task_redis
                executor.submit(run_task, task_id)
