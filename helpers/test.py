import datetime
import unittest
from random import random
import jdatetime
from django.core.exceptions import ValidationError
from django.core.management import call_command
from faker import Faker
from rest_framework.test import APIClient
from helpers.validators import ModelValidator


class ITestCase(unittest.TestCase, APIClient):
    faker = Faker('fa_IR')
    fixtures = []

    def setUp(self):
        # call_command('loaddata', 'fixtures/accounts.json', verbosity=0)
        # call_command('loaddata', 'fixtures/companies.json', verbosity=0)
        for fixture in self.fixtures:
            call_command('loaddata', fixture, verbosity=0)
        self.client = APIClient()
        return super().setUp()

    @staticmethod
    def get_fake_phone_number():
        while True:
            phone = '09' + str(int(random() * 10**9))
            try:
                ModelValidator.phone_validator(phone)
                break
            except ValidationError:
                continue
        return phone

    @staticmethod
    def get_fake_jalali_date():
        date = datetime.datetime.strptime(ITestCase.faker.date(), "%Y-%m-%d")
        date = jdatetime.date.fromgregorian(date=date).strftime("%Y-%m-%d")
        return date


