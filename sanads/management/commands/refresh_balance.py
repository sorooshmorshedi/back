import datetime

from django.core.management.base import BaseCommand, CommandParser

from accounts.accounts.models import AccountBalance
from helpers.db import queryset_iterator
from helpers.functions import get_object_accounts
from helpers.middlewares.modify_request_middleware import ModifyRequestMiddleware
from sanads.models import SanadItem
from server.settings import BASE_DIR
from users.models import User
import os


class Command(BaseCommand):
    help = 'refresh accounts balance'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('user_id', type=int)

    def __init__(self):
        super().__init__()

        self.backups_directory = "{}/backups/refresh_balance".format(
            BASE_DIR,
        )

    def backup_balances(self):
        print("Backup balances")

        from django.core import serializers

        data = serializers.serialize('json', AccountBalance.objects.all())

        backup_directory = "{}/{}".format(self.backups_directory, datetime.date.today())
        if not os.path.exists(backup_directory):
            os.makedirs(backup_directory)

        path = "{}/{}.json".format(
            backup_directory,
            str(datetime.datetime.now().strftime("%H%M"))
        )

        with open(path, "w") as backup_file:
            backup_file.write(data)

    def delete_balances(self, user):
        print("Deleting all balances in financial year #{}".format(user.active_financial_year.id))
        AccountBalance.objects.filter(financial_year=user.active_financial_year).delete()

    def handle(self, *args, **options):
        user = User.objects.get(pk=options['user_id'])

        self.backup_balances()

        print("Set {} as performer user".format(user.username))
        ModifyRequestMiddleware.thread_local = type('thread_local', (object,), {
            'user': user
        })

        self.delete_balances(user)

        print("Update balances")
        qs = SanadItem.objects.filter(
            financial_year=user.active_financial_year,
        ).all()
        for item in queryset_iterator(qs):
            AccountBalance.update_balance(
                financial_year=item.financial_year,
                **get_object_accounts(item),
                bed_change=item.bed,
                bes_change=item.bes
            )

        print("Done!")
