from django.apps import AppConfig


class SanadConfig(AppConfig):
    name = 'sanads'

    def ready(self):
        import sanads.sanads.signals
        import sanads.transactions.signals
