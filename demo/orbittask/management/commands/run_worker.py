from django.core.management.base import BaseCommand
from redis.exceptions import TimeoutError as RedisTimeoutError
from concurrent.futures import ThreadPoolExecutor
from orbittask.models import Task
from orbittask.conf import get_redis
from orbittask.registry import TASK_registery


redis = get_redis()

def get_task(id):
    return Task.objects.get(id=id)

def run_task(task_id):
    task = get_task(int(task_id))
    func = TASK_registery.get(task.name)
    func(*task.args, **task.kwargs)

class Command(BaseCommand):
    def handle(self, *args, **options):
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
