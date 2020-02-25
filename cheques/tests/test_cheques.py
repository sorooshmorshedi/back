import django

from accounts.tests.test_accounts import AccountTest
from cheques.models.ChequeModel import Cheque

django.setup()

from users.models import User

from django.urls.base import reverse
from rest_framework import status

from helpers.test import ITestCase


class ChequeTest(ITestCase):
    data = {
        "received_or_paid": "r",
        "due": "1398-12-06",
        "date": "1398-12-06",
        "serial": "1522",
        "account": 617,
        "value": 1500000
    }

    def test_cheque(self):
        user = User.objects.first()
        self.client.force_authenticate(user)

        cheque_id = self._test_create_cheque()
        self._test_get_cheques()
        self._test_update_cheque(cheque_id)
        self._test_delete_cheque(cheque_id)

    def _test_create_cheque(self):
        response = self.client.post(reverse('receivedCheque-list'), data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data
        cheque = Cheque.objects.get(pk=data['id'])

        return cheque.id

    def _test_get_cheques(self):
        response = self.client.get(reverse('receivedCheque-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        self.assertEqual(len(data), Cheque.objects.filter(received_or_paid=Cheque.RECEIVED).count())

    def _test_update_cheque(self, cheque_id):
        response = self.client.put(reverse('receivedCheque-detail', args=[cheque_id]), data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _test_delete_cheque(self, cheque_id):
        response = self.client.delete(reverse('receivedCheque-detail', args=[cheque_id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
