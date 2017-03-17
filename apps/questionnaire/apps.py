from django.apps import AppConfig


class ProfileConfig(AppConfig):
    name = 'questionnaire'

    def ready(self):
        import apps.questionnaire.signals.handlers