from django.core.management.base import BaseCommand
from factors.models import Factor


class Command(BaseCommand):
    help = 'Tmp command, for testing, correcting, bug fixing and etc'

    def handle(self, *args, **options):
        for item in Factor.objects.all():
            item.save()
