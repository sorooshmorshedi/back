from django.apps import AppConfig


class TransactionConfig(AppConfig):
    name = 'transactions'

    def ready(self):
        pass
