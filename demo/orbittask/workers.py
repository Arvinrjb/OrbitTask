from orbittask.models import Task
from orbittask.conf import get_redis
from orbittask.registry import TASK_registery
from concurrent.futures import ThreadPoolExecutor


redis = get_redis()

def get_task(id):
    return Task.objects.get(id=id)


def run_worker():
    with ThreadPoolExecutor(max_workers=4) as executor:
        while True:
            task_redis = redis.brpop("orbittask:queue", timeout=5)
            if task_redis is None:
                continue

            _, task_id = task_redis
            task = get_task(int(task_id))
            func = TASK_registery.get(task.name)
            executor.submit(func, *task.args, **task.kwargs)


if __name__ == "__main__":
    run_worker()
