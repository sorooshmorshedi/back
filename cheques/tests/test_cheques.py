from accounts.tests.test_accounts import AccountTest
from cheques.models.ChequeModel import Cheque
from users.models import User

from django.urls.base import reverse
from rest_framework import status

from helpers.test import MTestCase
from users.tests.test_users import UserTest


class ChequeTest(MTestCase):

    @property
    def data(self):

        account, float_account_id, cost_center_id = AccountTest.get_account()

        return {
            "received_or_paid": "r",
            "due": "1398-12-06",
            "date": "1398-12-06",
            "serial": "1522",
            "account": account.id,
            "floatAccount": float_account_id,
            "costCenter": cost_center_id,
            "value": 1500000
        }

    def test_cheque(self):
        user = UserTest.get_user()
        self.client.force_authenticate(user)

        cheque_id = self._test_submit_cheque()
        self._test_update_cheque(cheque_id)
        self._test_delete_cheque(cheque_id)

    def _test_submit_cheque(self):
        response = self.client.post(reverse('submitCheque'), data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        cheque = Cheque.objects.get(pk=data['id'])

        return cheque.id

    def _test_update_cheque(self, cheque_id):
        response = self.client.put(reverse('chequeDetail', args=[cheque_id]), data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _test_delete_cheque(self, cheque_id):
        response = self.client.delete(reverse('chequeDetail', args=[cheque_id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
