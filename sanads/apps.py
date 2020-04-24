from django.apps import AppConfig


class SanadConfig(AppConfig):
    name = 'sanads'

    def ready(self):
        import sanads.signals
