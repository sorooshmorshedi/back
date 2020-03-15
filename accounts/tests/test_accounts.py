from django.core.management import call_command
from django.db.models.aggregates import Count

from helpers.test import MTestCase
from users.models import User

from accounts.accounts.models import Account

from django.urls.base import reverse
from rest_framework import status

from users.tests.test_users import UserTest


class AccountTest(MTestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserTest.get_user()
        cls.account = AccountTest.get_account()[0]

    def test_create_account(self):
        parent = self.get_account(level=Account.MOEIN)[0]

        self.client.force_authenticate(self.user)

        response = self.client.post(reverse('accounts'), data={
            'name': self.faker.name(),
            'account_type': Account.OTHER,
            'parent': parent.id,
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_account(self):
        account = self.get_account()[0]
        new_name = 'this is a new name'

        self.client.force_authenticate(self.user)

        response = self.client.put(reverse('accountDetail', args=[account.id]), data={
            'name': new_name,
            'account_type': Account.OTHER
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
        account = Account.objects.filter(level=level).first()

        float_account_id = cost_center_id = None
        if account.floatAccountGroup:
            float_account_id = account.floatAccountGroup.floatAccounts.first().id
        if account.costCenterGroup:
            cost_center_id = account.costCenterGroup.floatAccounts.first().id

        return account, float_account_id, cost_center_id
