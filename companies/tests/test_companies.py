import random

from django.urls import reverse
from rest_framework import status

from companies.models import Company
from helpers.test import MTestCase
from users.tests import UserTest


class CompanyTest(MTestCase):
    def test_create_company(self):
        user = UserTest.get_user()
        self.client.force_authenticate(user)

        company_name = self.faker.name()

        response = self.client.post(reverse('company-list'), data={
            'name': company_name
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_companies(self):
        user = UserTest.get_user()
        self.client.force_authenticate(user)

        company_name = self.faker.name()

        company = CompanyTest.create_company(company_name)

        response = self.client.get(reverse('company-detail', args=[company.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data['name'], company_name)

    def test_update_companies(self):
        user = UserTest.get_user()
        self.client.force_authenticate(user)
        company = CompanyTest.create_company()

        new_company_name = 'alia {}'.format(random.random())

        response = self.client.put(reverse('company-detail', args=[company.id]), data={
            'name': new_company_name
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data['name'], new_company_name)

    def test_delete_companies(self):
        user = UserTest.get_user()
        self.client.force_authenticate(user)
        company = CompanyTest.create_company()

        response = self.client.delete(reverse('company-detail', args=[company.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @staticmethod
    def create_company(name=None):
        name = name if name else MTestCase.faker.name()
        company = Company(
            name=name,
        )
        company.save()
        return company
