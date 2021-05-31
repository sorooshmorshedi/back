from django.core.management.base import BaseCommand
from django.db.models import Count

from _dashtbashi.models import Lading
from companies.models import Company, CompanyUser
from factors.factor_sanad import FactorSanad
from factors.models import Factor
from helpers.test import set_user


class Command(BaseCommand):
    help = 'Tmp command, for testing, correcting, bug fixing and etc'

    def handle(self, *args, **options):
        qs = Lading.objects.filter(
            financial_year__company_id=4
        ).values('lading_number').annotate(
            count=Count('id')
        ).values('lading_number').order_by().filter(count__gt=1)

        print(list(qs))
