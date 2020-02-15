import django
from django.db.models.aggregates import Count

django.setup()

from users.models import User

from accounts.accounts.models import Account

from django.urls.base import reverse
from rest_framework import status

from helpers.test import ITestCase


class AccountTest(ITestCase):

    def test_create_account(self):
        parent = Account.objects.filter(level=Account.MOEIN).first()

        user = User.objects.first()
        self.client.force_authenticate(user)

        response = self.client.post(reverse('accounts'), data={
            'name': self.faker.name(),
            'parent': parent.id,
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_account(self):
        account = self.get_account()
        new_name = self.faker.name()

        user = User.objects.first()
        self.client.force_authenticate(user)

        response = self.client.put(reverse('accountDetail', args=[account.id]), data={
            'name': new_name
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data['name'], new_name)

    def test_delete_account(self):
        self.test_create_account()

        account = Account.objects.annotate(
            sanads_count=Count('sanadItems'),
            default_accounts_count=Count('defaultAccounts'),
        ).filter(
            level=Account.TAFSILI,
            sanads_count=0,
            default_accounts_count=0
        ).last()

        user = User.objects.first()
        self.client.force_authenticate(user)

        response = self.client.delete(reverse('accountDetail', args=[account.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_account(level=Account.TAFSILI):
        return Account.objects.filter(level=level).first()
