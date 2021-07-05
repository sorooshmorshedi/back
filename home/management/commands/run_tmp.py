from django.core.management.base import BaseCommand
from django.db.models import Count

from _dashtbashi.models import Lading
from companies.models import Company, CompanyUser, FinancialYear
from factors.factor_sanad import FactorSanad
from factors.models import Factor
from helpers.test import set_user
from sanads.models import Sanad
from transactions.models import Transaction


class Command(BaseCommand):
    help = 'Tmp command, for testing, correcting, bug fixing and etc'

    def handle(self, *args, **options):
        for company in Company.objects.all():
            set_user(company.created_by)

            print("#{}".format(company.id))

            models = [Sanad, Transaction]
            for model in models:
                for item in model.objects.filter(financial_year__company=company):
                    if item.financial_year.check_date(item.date, raise_exception=False):
                        item.define()
