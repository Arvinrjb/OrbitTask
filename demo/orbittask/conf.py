from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework.permissions import AllowAny


def get_permission_classes():
    classes = getattr(settings, "ORBITTASK_PERMISSION_CLASSES", None)
    perms = []
    result = []

    if classes is None:
        return [AllowAny()]
    
    for pc in classes:
        if isinstance(pc, str):
            perms.append(import_string(pc))
        else:
            perms.append(pc)

    for perm in perms:
        result.append(perm())
    return result
