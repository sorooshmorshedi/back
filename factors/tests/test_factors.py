import django

django.setup()

from users.models import User

from django.urls.base import reverse
from rest_framework import status

from helpers.test import ITestCase


class FactorTest(ITestCase):
    data = {
        "factor": {
            "taxPercent": 0,
            "taxValue": 0,
            "discountPercent": 0,
            "discountValue": 0,
            "expenses": [],
            "date": "1398-11-26",
            "time": "14:48",
            "account": 492,
            "type": "buy"
        },
        "factor_items": {
            "items": [{
                "discountValue": 0,
                "discountPercent": 0,
                "fee": "1600000",
                "is_editable": True,
                "ware": 2,
                "warehouse": 1,
                "count": "2"
            }],
            "ids_to_delete": []
        },
        "factor_expenses": {
            "items": [{
                "expense": 1,
                "value": "123",
                "account": 491,
                "explanation": "sdf"
            }],
            "ids_to_delete": []
        }
    }

    def test_factor(self):
        user = User.objects.first()
        self.client.force_authenticate(user)

        factor_id = self._test_create_factor()
        self._test_update_factor(factor_id)
        self._test_delete_factor(factor_id)

    def _test_create_factor(self):
        response = self.client.post(reverse('factor-list'), data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        return response.data['id']

    def _test_update_factor(self, factor_id):
        response = self.client.put(reverse('factor-detail', args=[factor_id]), data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _test_delete_factor(self, factor_id):
        response = self.client.delete(reverse('factor-detail', args=[factor_id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

