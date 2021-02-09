from django.core.management.base import BaseCommand
from django.db.models import Q, F

from helpers.db import queryset_iterator
from helpers.test import set_user
from sanads.models import SanadItem


class Command(BaseCommand):
    help = 'Tmp command, for testing, correcting, bug fixing and etc'

    def handle(self, *args, **options):
        for item in queryset_iterator(SanadItem.objects.filter(
                ~Q(is_auto_created=F('sanad__is_auto_created'))
        ).prefetch_related('sanad').all()):
            print(item.id)
            set_user(item.created_by)
            item.is_auto_created = item.sanad.is_auto_created
            item.save()
