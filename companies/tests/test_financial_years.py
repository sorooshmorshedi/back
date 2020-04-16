import random

import jdatetime
from django.urls import reverse
from rest_framework import status

from companies.models import Company, FinancialYear
from companies.tests.test_companies import CompanyTest
from helpers.test import MTestCase
from users.tests import UserTest


class FinancialYearTest(MTestCase):
    def test_create_financial_year(self):
        user = UserTest()
        company = CompanyTest.create_company()
        self.client.force_authenticate(user)

        name = self.faker.name()
        start = jdatetime.date.today()
        end = start + jdatetime.timedelta(days=365)

        response = self.client.post(reverse('financial-year-list'), data={
            'name': name,
            'start': start.isoformat(),
            'end': end.isoformat(),
            'company': company.id
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_financial_year(self):
        user = UserTest.get_user()
        self.client.force_login(user)
        company = CompanyTest.create_company()
        financial_year = FinancialYearTest.create_financial_year(company)

        response = self.client.get(reverse('financial-year-detail', args=[financial_year.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data['name'], financial_year.name)

    def test_update_financial_year(self):
        user = UserTest.get_user()
        self.client.force_login(user)
        company = CompanyTest.create_company()
        financial_year = FinancialYearTest.create_financial_year(company)

        new_name = 'sep {}'.format(random.random())

        response = self.client.patch(reverse('financial-year-detail', args=[financial_year.id]), data={
            'name': new_name,
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data['name'], new_name)

    def test_delete_financial_year(self):
        user = UserTest.get_user()
        self.client.force_login(user)
        company = CompanyTest.create_company()
        financial_year = FinancialYearTest.create_financial_year(company)

        response = self.client.delete(reverse('financial-year-detail', args=[financial_year.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @staticmethod
    def create_financial_year(company, name=None, start=None, end=None) -> FinancialYear:
        name = name if name else MTestCase.faker.name()
        start = start if start else jdatetime.date.today()
        end = end if end else jdatetime.date.today() + jdatetime.timedelta(days=365)
        financial_year = FinancialYear(
            company=company,
            name=name,
            start=start,
            end=end
        )
        financial_year.save()
        return financial_year
