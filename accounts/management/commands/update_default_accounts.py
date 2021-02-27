import json
from django.core.management.base import BaseCommand
from django.db.models import Q

from accounts.defaultAccounts.models import DefaultAccount
from companies.models import FinancialYear, Company
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

        with open(BASE_DIR + '/home/fixtures/dashtbashi.json', 'rb') as fixture_file:
            fixture_data += json.load(fixture_file)

        items = list(filter(lambda x: x['model'] == 'accounts.defaultaccount', fixture_data))

        for item in items:
            fields = item['fields']
            codename = fields['codename']

            if not codename:
                continue

            excluded_fields = ('financial_year', 'codename', 'account', 'floatAccount', 'costCenter')
            for field in excluded_fields:
                if field in fields:
                    del fields[field]

            print("Codename: {}".format(codename))
            for company in Company.objects.all():
                financial_year = company.financial_years.latest()
                print(" - Company #{}".format(company.id))
                try:
                    item = DefaultAccount.objects.filter(financial_year__company=company).get(codename=codename)
                    item.update(**fields)
                except DefaultAccount.MultipleObjectsReturned:
                    print(" - - Duplicate {}!".format(codename))
                    qs = DefaultAccount.objects.filter(financial_year__company=company, codename=codename).order_by('pk')
                    item = qs.first()
                    item.update(**fields)
                    print(" - - ", qs.filter(~Q(pk=item.id)).delete())
                except DefaultAccount.DoesNotExist:
                    print(" - - Creating Default Account")
                    DefaultAccount.objects.create(financial_year=financial_year, codename=codename, **fields)
