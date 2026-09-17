from django.apps import AppConfig


class OrbittaskConfig(AppConfig):
    name = 'orbittask'
    default = True
    def ready(self):
        import orbittask.tasks
