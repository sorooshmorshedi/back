from django.core.management.base import BaseCommand
from django.db.models import F, Q

from _dashtbashi.models import Lading
from _dashtbashi.sanads import LadingSanad
from helpers.middlewares.ModifyRequestMiddleware import ModifyRequestMiddleware
from users.models import User


class Command(BaseCommand):
    help = 'Tmp command, for testing, correcting, bug fixing and etc'

    def handle(self, *args, **options):
        ModifyRequestMiddleware.thread_local = type('thread_local', (object,), {'user': User.objects.get(pk=3)})

        for lading in Lading.objects.filter(~Q(sanad_date=F('sanad__date'))).all():
            print(lading.id)
            LadingSanad(lading).update()
