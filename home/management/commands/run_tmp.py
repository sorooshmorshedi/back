from django.core.management.base import BaseCommand
from django.db.models import Count

from _dashtbashi.models import Lading
from companies.models import Company, CompanyUser, FinancialYear
from factors.factor_sanad import FactorSanad
from factors.models import Factor
from helpers.test import set_user
from sanads.models import Sanad


class Command(BaseCommand):
    help = 'Tmp command, for testing, correcting, bug fixing and etc'

    def handle(self, *args, **options):
        for company in Company.objects.all():
            set_user(company.created_by)

            print("#{}".format(company.id))
            for sanad in Sanad.objects.filter(financial_year__company=company):
                if sanad.financial_year.check_date(sanad.date, raise_exception=False):
                    sanad.define()
