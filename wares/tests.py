from helpers.test import MTestCase
from wares.models import Ware


class WareTest(MTestCase):

    @staticmethod
    def get_ware():
        ware = Ware.objects.first()
        return ware
