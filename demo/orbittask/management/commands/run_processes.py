import json
from django.core.management.base import BaseCommand
from redis.exceptions import TimeoutError as RedisTimeoutError
from concurrent.futures import ProcessPoolExecutor
from orbittask.conf import get_redis
from orbittask.registry import TASK_registery_process


# get object from database and get functions from TASK_registery 
def get_task(id):
    import django
    django.setup()
    from orbittask.models import Task
    try:
        obj = Task.objects.get(id=id)
        func = TASK_registery_process.get(obj.registry)
        return obj, func
    except Task.DoesNotExist:
        raise Exception("Error while get Task")

# run task function
def run_task(task_id):
    from django.utils import timezone
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
    def add_arguments(self, parser):
        parser.add_argument(
            "--process",
            type=int,
            default=2
        )

    def handle(self, *args, **options):
        process=options["process"]
        redis = get_redis()
        self.stdout.write("Worker started. Waiting for tasks...")
        self.stdout.write(f"Registered tasks: {list(TASK_registery_process.keys())}")
        # for I/O bound tasks
        with ProcessPoolExecutor(max_workers=process) as executor:
            while True:
                try:
                    task_redis = redis.brpop("orbittask:queue:process", timeout=5)
                except RedisTimeoutError:
                    continue

                if task_redis is None:
                    continue
                
                message = json.loads(task_redis[1])
                task_id = message["id"]
                executor.submit(run_task, task_id)

