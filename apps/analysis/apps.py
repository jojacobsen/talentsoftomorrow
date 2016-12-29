from django.apps import AppConfig


class AnalysisConfig(AppConfig):
    name = 'analysis'

    def ready(self):
        import apps.analysis.signals.handlers
