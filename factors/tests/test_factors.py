from random import randint

import jdatetime

from accounts.tests.test_accounts import AccountTest
from factors.models import Factor, FactorItem
from users.models import User

from django.urls.base import reverse
from rest_framework import status

from helpers.test import MTestCase
from wares.models import Ware
from wares.tests import WareTest


class FactorTest(MTestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.first()

    @property
    def data(self):
        account, float_account_id, cost_center_id = AccountTest.get_account()

        ware = Ware.objects.first()

        return {
            "item": {
                "taxPercent": 0,
                "taxValue": 0,
                "discountPercent": 0,
                "discountValue": 0,
                "expenses": [],
                "date": "1398-11-26",
                "time": "14:48",
                "account": account.id,
                "floatAccount": float_account_id,
                "costCenter": cost_center_id,
                "type": "buy"
            },
            "items": {
                "items": [{
                    "discountValue": 0,
                    "discountPercent": 0,
                    "fee": "1600000",
                    "ware": ware.id,
                    "warehouse": 1,
                    "count": "2"
                }],
                "ids_to_delete": []
            },
            "expenses": {
                "items": [],
                "ids_to_delete": []
            }
        }

    def test_create_factor(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse('factor-list'), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        return response.data['id']

    def test_update_factor(self):
        self.client.force_authenticate(self.user)
        factor_id = FactorTest.create_factor(self.user.active_financial_year, Factor.BUY).id
        response = self.client.put(reverse('factor-detail', args=[factor_id]), data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_factor(self):
        self.client.force_authenticate(self.user)
        factor_id = FactorTest.create_factor(self.user.active_financial_year, Factor.BUY).id
        response = self.client.delete(reverse('factor-detail', args=[factor_id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @staticmethod
    def create_factor(financial_year, factor_type):
        account, float_account_id, cost_center_id = AccountTest.get_account()
        factor = Factor.objects.create(
            type=factor_type,
            account=account,
            floatAccount_id=float_account_id,
            costCenter_id=cost_center_id,
            date=jdatetime.date.today(),
            time=jdatetime.datetime.now().strftime('%H:%m'),
            financial_year=financial_year
        )
        return factor

    @staticmethod
    def create_factor_item(factor: Factor, **kwargs):
        ware = kwargs.get('ware', WareTest.get_ware())
        warehouse = kwargs.get('warehouse', ware.warehouse)
        count = kwargs.get('count', randint(5, 20))
        fee = kwargs.get('fee', randint(1, 10) * 1000)
        factor_item = FactorItem.objects.create(
            factor=factor,
            ware=ware,
            warehouse=warehouse,
            count=count,
            fee=fee,
            financial_year=factor.financial_year
        )
        return factor_item
