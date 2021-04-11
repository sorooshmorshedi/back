import json

from django.core.management.base import BaseCommand
from django.db.models import Q

from companies.models import FinancialYear
from factors.factor_sanad import FactorSanad
from factors.models import Factor
from helpers.test import set_user
from home.models import DefaultText
from server.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Tmp command, for testing, correcting, bug fixing and etc'

    def handle(self, *args, **options):
        self.check_factors_sanads()

    def check_factors_sanads(self):
        qs = Factor.objects.filter(
            ~Q(type__in=(Factor.INPUT_TRANSFER, Factor.OUTPUT_TRANSFER)),
            financial_year_id=4,
            is_definite=True,
        )
        for factor in qs:
            has_account = False

            account_value = 0
            sanad_items = factor.sanad.items.all()
            for sanad_item in sanad_items:
                if sanad_item.account_id == 1764:
                    has_account = True
                    if factor.type in Factor.OUTPUT_GROUP:
                        value = sanad_item.bes
                    else:
                        value = sanad_item.bed
                    account_value += value

            if account_value != factor.calculated_sum:
                print(factor.id, factor.type)
                print(" - Wrong value: {} != {}".format(account_value, factor.calculated_sum))

            if not has_account:
                print(" - {} Factor {}'s sanad ({}) does not have the account".format(
                    factor.type,
                    factor.id,
                    factor.sanad_id
                ))

    def add_default_texts(self):
        with open(BASE_DIR + '/home/fixtures/6-default_texts.json', 'rb') as fixture_file:
            fixture_data = json.load(fixture_file)

            for financial_year in FinancialYear.objects.all().order_by('id'):
                print(financial_year.id)
                set_user(financial_year.created_by)

                if DefaultText.objects.inFinancialYear(financial_year).count() == 0:

                    for item in fixture_data:
                        fields = item['fields'].copy()
                        fields['pk'] = None
                        fields['financial_year'] = financial_year
                        DefaultText.objects.create(**fields)

    def update_all_factors_sanads(self):
        i = 0
        qs = Factor.objects.filter(is_definite=True)
        count = qs.count()
        for factor in qs:
            print("{}/{} : {}".format(count, i + 1, factor.id))
            set_user(factor.created_by)
            try:
                FactorSanad(factor).update(True)
            except Exception as e:
                print(e)
            i += 1
