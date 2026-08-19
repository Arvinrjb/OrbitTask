from django.apps import AppConfig


class OrbittaskConfig(AppConfig):
    name = 'orbittask'

    def ready(self):
        import orbittask.tasks
