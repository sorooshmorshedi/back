from django.apps import AppConfig


class ChequesConfig(AppConfig):
    name = 'cheques'

    def ready(self):
        import cheques.signals
