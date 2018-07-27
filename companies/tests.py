from random import random

import json

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework_jwt.settings import api_settings

from companies.models import Company


class CompanyModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='mmd', email='testi@gmail.com', password='mmdadmin')

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        self.token = 'JWT ' + jwt_encode_handler(payload)

        self.client = Client(HTTP_AUTHORIZATION=self.token)

    def createCompany(self):
        c = Company(name='temp' + str(random()),
                    fiscal_year_start='2004-03-04',
                    fiscal_year_end='2005-03-04',
                    )
        c.save()
        return c

    def test_get_companies(self):
        self.client.force_login(self.user)
        res = self.client.get(reverse('companies'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_company(self):
        self.client.force_login(self.user)
        res = self.client.post(reverse('companies'), {
            'name': 'cpm3-3',
            'fiscal_year_start': '2004-03-04',
            'fiscal_year_end': '2005-03-04',
            'address1': 'adas asdf',
            'address2': 'adsfas 2ew',
            'country': 'Iran',
            'sabt_number': '123123123',
            'phone1': '123123',
            'phone2': '1232312',
            'fax': '123123213',
            'email': 'sirmmds@gmail.com',
            'website': 'http://www.tbywe.com',
            'postal_code': '12312',
            'eghtesadi_code': '1232',
            'shenase': '12312',
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_get_detail(self):
        self.createCompany()
        res = self.client.get(reverse('companyDetail', kwargs={'id': 1}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_company(self):
        self.createCompany()
        res = self.client.put(
            reverse('companyDetail', kwargs={'id': 1}),
            # '/companies/1',
            content_type='application/json',
            data=json.dumps({
                'name': 'newName',
                'fiscal_year_start': '2004-03-04',
                'fiscal_year_end': '2005-03-14',
            })
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

