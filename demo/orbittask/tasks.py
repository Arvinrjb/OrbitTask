from orbittask.decorators import task


# Example Task functions 
@task
def hello():
    print("Hello world")

@task
def sum(x, y):
    print(f"result is {x + y}")