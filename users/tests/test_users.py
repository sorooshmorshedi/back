from django.urls.base import reverse
from rest_framework import status

from helpers.test import ITestCase
from users.models import User


class UserTest(ITestCase):

    def test_retrieve_user(self):
        user = UserTest.create_user()
        self.client.force_authenticate(user)

        response = self.client.get(reverse('retrieve-user'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()

    def test_set_active_company(self):
        user = UserTest.create_user()
        self.client.force_authenticate(user)

        from companies.tests.test_companies import CompanyTest
        company = CompanyTest.create_company()

        response = self.client.post(reverse('set-active-company'), data={
            'company': company.id
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.active_company.id, company.id)

        self.client.logout()

    def test_set_active_financial_year(self):
        # todo: fill this function
        pass

    @staticmethod
    def create_user(username=None, password='123abc456'):
        username = username if username else ITestCase.faker.name()
        user = User.objects.create_user(username, password=password)
        return user


