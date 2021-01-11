import json
from django.core.management.base import BaseCommand

from accounts.defaultAccounts.models import DefaultAccount
from companies.models import FinancialYear
from helpers.middlewares.ModifyRequestMiddleware import ModifyRequestMiddleware
from server.settings import BASE_DIR
from users.models import User


class Command(BaseCommand):
    help = 'Update default accounts without changing codename, account, floatAccount & costCenter fields'

    def handle(self, *args, **options):
        user = User.objects.filter(is_staff=True).first()
        ModifyRequestMiddleware.thread_local = type('thread_local', (object,), {
            'user': user
        })

        with open(BASE_DIR + '/home/fixtures/3-accounts.json', 'rb') as fixture_file:
            fixture_data = json.load(fixture_file)

        items = list(filter(lambda x: x['model'] == 'accounts.defaultaccount', fixture_data))

        for item in items:
            fields = item['fields']
            codename = fields['codename']

            if not codename:
                continue

            del fields['financial_year']
            del fields['codename']
            del fields['account']
            if 'floatAccount' in fields:
                del fields['floatAccount']
            if 'costCenter' in fields:
                del fields['costCenter']

            for financial_year in FinancialYear.objects.all():
                try:
                    item = DefaultAccount.objects.get(financial_year=financial_year, codename=codename)
                    item.update(**fields)
                except DefaultAccount.DoesNotExist:
                    DefaultAccount.objects.create(financial_year=financial_year, codename=codename, **fields)
