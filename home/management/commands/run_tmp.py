from django.contrib.admin.options import get_content_type_for_model
from django.core.management.base import BaseCommand
from _dashtbashi.models import Lading, OilCompanyLading
from cheques.models.StatusChangeModel import StatusChange
from companies.models import Company
from factors.models import Factor, Transfer, Adjustment
from helpers.test import set_user
from imprests.models import ImprestSettlement
from sanads.models import Sanad
from transactions.models import Transaction


class Command(BaseCommand):
    help = 'Tmp command, for testing, correcting, bug fixing and etc'

    def handle(self, *args, **options):
        self.update_sanads_origin()

    def update_sanads_origin(self):
        for company in Company.objects.all():
            set_user(company.created_by)

            print("#{}".format(company.id))

            models = [Factor, Transaction, Adjustment, Lading, OilCompanyLading, StatusChange, ImprestSettlement]
            for model in models:
                for item in model.objects.filter(financial_year__company=company):
                    if model == Lading:
                        date = item.sanad_date
                    else:
                        date = item.date
                    if item.financial_year.check_date(date, raise_exception=False) and getattr(item, 'sanad', None):
                        sanad = item.sanad
                        content_type = get_content_type_for_model(model)

                        sanad.origin_content_type = content_type
                        sanad.origin_id = item.id
                        sanad.items.update(origin_content_type=content_type, origin_id=item.id)
                        sanad.save()

    def define_all_definable_models(self):
        for company in Company.objects.all():
            set_user(company.created_by)

            print("#{}".format(company.id))

            models = [Sanad, Transaction, Transfer, Adjustment, ]
            for model in models:
                for item in model.objects.filter(financial_year__company=company):
                    if item.financial_year.check_date(item.date, raise_exception=False):
                        item.define()
