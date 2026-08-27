from functools import wraps
from orbittask.registry import TASK_registery_thread, TASK_registery_process


def task_thread(func):
    name = f"{func.__qualname__}"
    TASK_registery_thread[name] = func
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    # wrapper.name = name
    return wrapper

def task_process(func):
    name = f"{func.__qualname__}"
    TASK_registery_process[name] = func
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    # wrapper.name = name
    return wrapper
