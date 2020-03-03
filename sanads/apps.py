from django.apps import AppConfig


class SanadConfig(AppConfig):
    name = 'sanad'

    def create(self):
        import sanads.sanads.signals
        import sanads.transactions.signals
