import datetime

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandParser

from factors.models import FactorItem, Factor
from factors.views.definite_factor import DefiniteFactor
from helpers.db import queryset_iterator, bulk_create
from helpers.middlewares.ModifyRequestMiddleware import ModifyRequestMiddleware
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

        self.backup_inventory()

        print("Set {} as performer user".format(user.username))
        ModifyRequestMiddleware.thread_local = type('thread_local', (object,), {
            'user': user
        })

        self.delete_inventories(user)

        print("Undo + Redo definition")
        qs = Factor.objects.filter(
            financial_year=user.active_financial_year,
            is_definite=True
        ).all()
        for factor in queryset_iterator(qs, key=('definition_date',)):
            DefiniteFactor.updateFactorInventory(factor)

        print("Done!")
