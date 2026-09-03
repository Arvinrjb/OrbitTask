import threading
import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from redis.exceptions import TimeoutError as RedisTimeoutError
from concurrent.futures import ThreadPoolExecutor
from orbittask.models import Task, Logs
from orbittask.conf import get_redis
from orbittask.registry import TASK_registery_thread


redis = get_redis()
threading_event = threading.Event()

def delay_thread():
    while not threading_event.is_set():
        now = timezone.now().timestamp()     
        tasks = redis.zrangebyscore(
            "orbittask:delayed",
            min=0,
            max=now
        )
        
        pipe = redis.pipeline(transaction=True)
        for row in tasks:
            task = json.loads(row)
            task["eta"] = None
            pipe.zrem("orbittask:delayed", row)
            pipe.lpush("orbittask:queue:thread", json.dumps(task))
        pipe.execute()        
        threading_event.wait(timeout=1)


def start_delay_thread():
    thread = threading.Thread(target=delay_thread)
    thread.start()
    return thread

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
        thread = start_delay_thread() 
        workers=options["workers"]
        self.stdout.write("Worker started. Waiting for tasks...")
        self.stdout.write(f"Registered tasks: {list(TASK_registery_thread.keys())}")
        # for I/O bound tasks
        try:
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
                    if message["eta"]:
                        eta_timestamp = parse_datetime(message["eta"]).timestamp()
                        redis.zadd("orbittask:delayed", {json.dumps(message):eta_timestamp})
                    else:
                        executor.submit(run_task, task_id)
        except KeyboardInterrupt:
            pass
        finally:
            threading_event.set()
            thread.join()