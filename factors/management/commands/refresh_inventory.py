import datetime
from django.core.management.base import BaseCommand, CommandParser
from rest_framework.exceptions import ValidationError

from factors.models import Factor
from factors.views.definite_factor import DefiniteFactor
from helpers.db import queryset_iterator
from helpers.middlewares.modify_request_middleware import ModifyRequestMiddleware
from sanads.serializers import FactorSanadSerializer
from server.settings import BASE_DIR
from users.models import User
from wares.models import WareInventory
import os


class Command(BaseCommand):
    help = 'refresh inventory'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('user_id', type=int)

    def __init__(self):
        super().__init__()

        self.backups_directory = "{}/backups/refresh_inventory".format(
            BASE_DIR,
        )

    def backup_inventory(self):
        print("Backup inventory")

        from django.core import serializers

        data = serializers.serialize('json', WareInventory.objects.all())

        backup_directory = "{}/{}".format(self.backups_directory, datetime.date.today())
        if not os.path.exists(backup_directory):
            os.makedirs(backup_directory)

        path = "{}/{}.json".format(
            backup_directory,
            str(datetime.datetime.now().strftime("%H%M"))
        )

        with open(path, "w") as backup_file:
            backup_file.write(data)

    def delete_inventories(self, user):
        print("Deleting all inventory records in financial year #{}".format(user.active_financial_year.id))
        WareInventory.objects.filter(financial_year=user.active_financial_year).delete()

    def handle(self, *args, **options):
        user = User.objects.get(pk=options['user_id'])
        financial_year = user.active_financial_year

        self.backup_inventory()

        print("Set {} as performer user".format(user.username))
        ModifyRequestMiddleware.thread_local = type('thread_local', (object,), {
            'user': user
        })

        self.delete_inventories(user)

        print("Undo + Redo definition")
        qs = Factor.objects.filter(
            financial_year=financial_year,
            is_definite=True
        ).all()

        errors = []
        for factor in queryset_iterator(qs, key=('definition_date',)):
            DefiniteFactor.updateFactorInventory(factor)

            for item in factor.items.all():
                print(item.remain_fees)
                for fee in item.remain_fees:
                    if fee['count'] < 0:
                        errors.append({
                            'ware_id': item.ware.id,
                            'ware_name': item.ware.name,
                            'warehouse_name': item.warehouse.name,
                            'count': abs(fee['count']),
                            'factor_item_order': item.order,
                            'factor': FactorSanadSerializer(factor).data
                        })

        if len(errors):
            raise ValidationError({'items': errors})

        financial_year.are_factors_sorted = True
        financial_year.save()

        print("Done!")
