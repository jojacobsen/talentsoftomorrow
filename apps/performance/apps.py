from django.apps import AppConfig


class PerformanceConfig(AppConfig):
    name = 'performance'

    def ready(self):
        from .signals import handlers
