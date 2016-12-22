from django.apps import AppConfig


class GeneticsConfig(AppConfig):
    name = 'genetics'

    def ready(self):
        from .signals import handlers
