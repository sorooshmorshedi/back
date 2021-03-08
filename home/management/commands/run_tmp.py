from decimal import Decimal

from django.core.management.base import BaseCommand

from factors.models import FactorItem
from helpers.test import set_user
from users.models import User
from wares.models import Ware, SalePriceType, SalePrice, Unit


class Command(BaseCommand):
    help = 'Tmp command, for testing, correcting, bug fixing and etc'

    def handle(self, *args, **options):
        set_user(User.objects.get(pk=1))

        print(SalePrice.objects.filter(conversion_factor=0).update(conversion_factor=1))
