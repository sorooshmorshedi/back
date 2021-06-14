from django.core.management.base import BaseCommand
from django.db.models import Count

from _dashtbashi.models import Lading
from companies.models import Company, CompanyUser, FinancialYear
from factors.factor_sanad import FactorSanad
from factors.models import Factor
from helpers.test import set_user


class Command(BaseCommand):
    help = 'Tmp command, for testing, correcting, bug fixing and etc'

    def handle(self, *args, **options):
        for financial_year in FinancialYear.objects.all():
            print("#{}".format(financial_year.id))
            factors = list(Factor.objects.inFinancialYear(financial_year).filter(code=0).order_by('id').all())
            if len(factors) > 2:
                for i in range(1, len(factors)):
                    factor = factors[i]
                    print(" - #{}".format(factor.id))
                    factor.delete()
