from time import sleep
from orbittask.decorators import task


# Example Task functions 
@task
def hello():
    sleep(5)
    print("Hello world")
    return "Hello world"

@task
def sum(x, y):
    print(f"result is {x + y}")
    return f"result is {x + y}"