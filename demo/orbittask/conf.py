import redis
from functools import lru_cache
from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework.permissions import Http404


def get_add_permission_classes():
    classes = getattr(settings, "ORBITTASK_ADD_PERMISSION_CLASSES", None)
    perms = []
    result = []

    if classes is None:
        return [Http404()]
    
    for pc in classes:
        if isinstance(pc, str):
            perms.append(import_string(pc))
        else:
            perms.append(pc)

    for perm in perms:
        result.append(perm())
    return result

def get_view_permission_classes():
    classes = getattr(settings, "ORBITTASK_VIEW_PERMISSION_CLASSES", None)
    perms = []
    result = []

    if classes is None:
        return [Http404()]
    
    for pc in classes:
        if isinstance(pc, str):
            perms.append(import_string(pc))
        else:
            perms.append(pc)

    for perm in perms:
        result.append(perm())
    return result

@lru_cache(maxsize=1)
def get_redis():
    url = getattr(settings, "ORBITTASK_REDIS_URL", "redis://localhost:6379/0")
    pool = redis.ConnectionPool.from_url(url, decode_responses=True)
    return redis.Redis(connection_pool=pool)