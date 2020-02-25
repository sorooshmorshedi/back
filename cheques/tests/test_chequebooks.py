import django

from accounts.tests.test_accounts import AccountTest
from cheques.models.ChequebookModel import Chequebook

django.setup()

from users.models import User

from django.urls.base import reverse
from rest_framework import status

from helpers.test import ITestCase


class ChequebookTest(ITestCase):
    data = {
        "account": AccountTest.get_account(3).id,
        "serial_from": 1,
        "serial_to": 5
    }

    def test_chequebook(self):
        user = User.objects.first()
        self.client.force_authenticate(user)

        chequebook_id = self._test_create_chequebook()
        self._test_get_chequebooks()
        self._test_update_chequebook(chequebook_id)
        self._test_delete_chequebook(chequebook_id)

    def _test_create_chequebook(self):
        response = self.client.post(reverse('chequebook-list'), data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data
        chequebook = Chequebook.objects.get(pk=data['id'])
        self.assertEqual(chequebook.cheques.count(), self.data['serial_to'] - self.data['serial_from'] + 1)

        return chequebook.id

    def _test_get_chequebooks(self):
        response = self.client.get(reverse('chequebook-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(len(data), Chequebook.objects.count())

    def _test_update_chequebook(self, chequebook_id):
        response = self.client.put(reverse('chequebook-detail', args=[chequebook_id]), data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def _test_delete_chequebook(self, chequebook_id):
        response = self.client.delete(reverse('chequebook-detail', args=[chequebook_id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
