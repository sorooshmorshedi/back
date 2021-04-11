from django.core.management.base import BaseCommand

from companies.models import FinancialYear
from home.models import DefaultText


class Command(BaseCommand):
    help = 'Tmp command, for testing, correcting, bug fixing and etc'

    def handle(self, *args, **options):
        try:
            base_financial_year = FinancialYear.objects.get(pk=21)
        except FinancialYear.DoesNotExist as e:
            base_financial_year = FinancialYear.objects.get(pk=1)

        for financial_year in FinancialYear.objects.all():
            if DefaultText.objects.inFinancialYear(financial_year).count() == 0:
                for item in DefaultText.objects.inFinancialYear(base_financial_year).all():
                    item.pk = None
                    item.financial_year = financial_year
                    item.save()
