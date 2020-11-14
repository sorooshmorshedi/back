import datetime
import json

from django.core.management import call_command
from django.core.management.base import BaseCommand

from factors.models import FactorItem
from factors.views.definite_factor import DefiniteFactor
from helpers.db import queryset_iterator, bulk_create
from helpers.middlewares.ModifyRequestMiddleware import ModifyRequestMiddleware
from server.settings import BASE_DIR
from users.models import User
from wares.models import WareInventory
import os


class Command(BaseCommand):
    help = 'refresh inventory'

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

    def restore_backup(self):

        os.chdir(self.backups_directory)
        folders = os.listdir()
        i = 0
        for folder in folders:
            print("({}) : {}".format(i, folder))
            i += 1
        selected_folder = folders[int(input("Enter folder: "))]

        os.chdir("{}/{}".format(self.backups_directory, selected_folder))
        files = os.listdir()
        i = 0
        for file in files:
            print("({}) : {}".format(i, file))
            i += 1
        selected_file = files[int(input("Enter file: "))]

        path = "{}/{}/{}".format(self.backups_directory, selected_folder, selected_file)

        self.delete_inventories()
        call_command("loaddata", path)

    def delete_inventories(self):
        print("Deleting all inventory records")
        WareInventory.objects.all().delete()

    def handle(self, *args, **options):
        print("Set admin use as performer user")
        ModifyRequestMiddleware.thread_local = type('thread_local', (object,), {
            'user': User.objects.filter(is_superuser=True, is_staff=True).first()
        })

        self.backup_inventory()

        self.delete_inventories()

        print("Inserting inventory records")
        qs = FactorItem.objects.filter(factor__is_definite=True).all()
        for item in queryset_iterator(qs):
            DefiniteFactor.updateInventory(item)

        print("Done!")
