# Attention
### This tool is still under development, and many features will be added to it in the future.
# Introduction

This is a Django app for managing processes and executing I/O bound and CPU bound tasks at various times.

### This tool has a demo version that can be used for testing.

# Installing
To install the dependencies, simply install the ones listed in the `requirements.txt` file.
```
pip install -r requirements.txt
```
In the settings file, we use two variables—`ORBITTASK_ADD_PERMISSION_CLASSES` and `ORBITTASK_VIEW_PERMISSION_CLASSES` to grant access permissions for the APIs; an example of this can be found in the demo.

And finally, add `orbittask` to the list of apps in the settings, and place the orbittask directory in the root directory.

# How To Use
### Add Task:
You just need to add the function to the `tasks.py` file and use the task decorator; an example is provided within the file.

### After adding the Task, simply use the following commands:
- For executing I/O bound Tasks
```
python manage.py run_thread --workers 4
```
- For executing CPU bound Tasks
```
python manage.py run_processes --process 4
```
### Finally, add the `api_urls.py` file to your API path and use the following APIs to add various tasks.
- To add tasks
#### /api/addtask
- To view the task
#### /api/viewtask
- To view the logs
#### /api/logs

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
