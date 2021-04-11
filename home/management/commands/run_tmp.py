from django.core.management.base import BaseCommand
from factors.factor_sanad import FactorSanad
from factors.models import Factor
from helpers.test import set_user


class Command(BaseCommand):
    help = 'Tmp command, for testing, correcting, bug fixing and etc'

    def handle(self, *args, **options):
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
