import random

from django.urls.base import reverse
from rest_framework import status

from helpers.test import MTestCase
from users.models import User


class UserTest(MTestCase):

    def test_create_user(self):
        user = UserTest.get_user()
        self.client.force_authenticate(user)

        response = self.client.post(reverse('create-user'), data={
            'username': 'mmd',
            'password': '1234'
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.logout()

    def test_update_user(self):
        user = UserTest.get_user()
        self.client.force_authenticate(user)

        response = self.client.put(reverse('update-user', args=[user.id]), data={
            'username': 'mmd',
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()

    def test_delete_user(self):
        user = UserTest.create_user()
        self.client.force_authenticate(user)

        response = self.client.delete(reverse('destroy-user', args=[user.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.client.logout()

    def test_user_change_password(self):
        self.client.force_authenticate(UserTest.get_user())
        user = self.create_user()

        response = self.client.post(reverse('change-user-password'), data={
            'user': user.id,
            'password': 'newPass'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()

    def test_list_users(self):
        user = UserTest.get_user()
        self.client.force_authenticate(user)

        for i in range(3):
            UserTest.create_user()

        response = self.client.get(reverse('list-users'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        self.client.logout()

    def test_retrieve_user(self):
        user = UserTest.get_user()
        self.client.force_authenticate(user)

        response = self.client.get(reverse('current-user'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()

    def test_set_active_company(self):
        user = UserTest.get_user()
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
    def get_user():
        user = User.objects.filter(is_superuser=True).first()
        return user

    @staticmethod
    def create_user(username=None, password=None):
        if not username:
            username = "{} - {}".format(MTestCase.faker.name(), random.random())
            password = MTestCase.faker.name()
        user = User.objects.create(
            username=username
        )
        user.set_password(password)
        user.save()
        return user
