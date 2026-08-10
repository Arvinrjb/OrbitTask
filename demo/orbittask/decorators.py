from functools import wraps
from orbittask.registry import TASK_registery


def task(func):
    name = f"{func.__qualname__}"
    TASK_registery[name] = func
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    # wrapper.name = name
    return wrapper
