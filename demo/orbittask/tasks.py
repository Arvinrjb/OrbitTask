from time import sleep
from orbittask.decorators import task_thread, task_process


# Example Task functions 
@task_thread
def hello():
    sleep(5)
    print("Hello world")
    return "Hello world"

@task_process
def sum(x, y):
    print(f"result is {x + y}")
    return f"result is {x + y}"