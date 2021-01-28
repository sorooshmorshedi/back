import inspect
from pprint import pprint

from django.apps import apps
from django.core.management.commands.dumpdata import Command as Dumpdata
from django.db.models.fields.related import RelatedField

from companies.models import FinancialYear


class Command(Dumpdata):

    def handle(self, *args, **kwargs):
        models = []
        apps_names = (
            'users',
            'companies',
            'accounts',
            'wares',
            'sanads',
            'transactions',
            'cheques',
            'factors',
            'reports',
            'home',
            'imprests',
            'sobhan_admin',
            '_dashtbashi',
        )

        for app_name in apps_names:
            models += apps.get_app_config(app_name).get_models()

        models = list(filter(lambda model: hasattr(model, 'financial_year'), models))

        for financial_year in FinancialYear.objects.all():

            for model in models:
                members = inspect.getmembers(model, lambda a: not (inspect.isroutine(a)))
                fields = [m[0] for m in members if not m[0].startswith('__')]

                anomaly_found = False
                for instance in model.objects.inFinancialYear(financial_year):
                    for field_name in fields:
                        try:
                            field = getattr(instance, field_name)
                        except:
                            continue
                        if hasattr(field, 'financial_year'):
                            field_financial_year = getattr(field, 'financial_year')
                            if field_financial_year.company != financial_year.company:
                                print("Anomaly found: {}.{}.{}.financial_year = {}, expected {}".format(
                                    model.__name__,
                                    instance.id,
                                    field_name,
                                    field_financial_year.id,
                                    financial_year.id
                                ))
                                anomaly_found = True
                                break

                    if anomaly_found:
                        break
