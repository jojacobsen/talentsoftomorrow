from django.apps import AppConfig


class GeneticsConfig(AppConfig):
    name = 'genetics'

    def ready(self):
        import apps.genetics.signals.handlers
