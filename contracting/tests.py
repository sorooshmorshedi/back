from rest_framework.reverse import reverse

from helpers.test import MTestCase

from rest_framework import status

from rest_framework.test import APIClient

from users.models import User

from faker import Faker

from contracting.models import Tender, Contract, Statement, Supplement


class TenderTest(MTestCase):
    @staticmethod
    def create_tender():
        fake = Faker()
        tender = Tender.objects.create(
            code=1,
            title="energy",
            explanation=fake.text(),
            province=fake.city(),
            classification="w",
            bidder=fake.company(),
            bidder_address=fake.address(),
            bidder_postal_code="1234567890"
        )
        return tender

    @property
    def data(self):
        fake = Faker()
        return {
            "code": 2,
            "title": "base",
            "explanation": fake.text(),
            "province": fake.city(),
            "city": 'shiraz',
            "classification": "w",
            "bidder": fake.company(),
            "bidder_address": fake.address(),
            "bidder_postal_code": "1234567890"
        }

    def test_get_all_tender(self):
        client = APIClient()
        user = User.objects.all().first()
        self.client.force_authenticate(user)
        response = self.client.get(reverse('tenderApi'), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_tender(self):
        client = APIClient()
        user = User.objects.all().first()
        self.client.force_authenticate(user)
        data = self.data
        url = '/contracting/tender/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_tender(self):
        self.create_tender()
        client = APIClient()
        user = User.objects.all().first()
        self.client.force_authenticate(user)
        url = '/contracting/tender/1/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ContractTest(MTestCase):

    @staticmethod
    def create_contract():
        contract = Contract.objects.create(
            title='gas',
            code=1,
            amount=0.00001,
        )
        return contract

    @property
    def data(self):
        return {
            "title": "fuel",
            "code": 1,
            "amount": 0.0003,
            "max_change_amount": 2,
            "doing_job_well": 2,
            "insurance_payment": 3,
            "other": 5

        }

    def test_get_all_contract(self):
        client = APIClient()
        user = User.objects.all().first()
        self.client.force_authenticate(user)
        url = '/contracting/contract/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

    def test_create_contract(self):
        client = APIClient()
        user = User.objects.all().first()
        self.client.force_authenticate(user)
        response = self.client.post(reverse('contractApi'), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_contract(self):
        self.create_contract()
        client = APIClient()
        user = User.objects.all().first()
        self.client.force_authenticate(user)
        url = '/contracting/contract/1/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class StatementTest(MTestCase):
    @staticmethod
    def create_statement():
        fake = Faker()
        cn = Contract.objects.create(title='hybrid', code=1, amount=0.00001)
        statement = Statement.objects.create(
            code=1,
            type='n',
            contract=cn,
            value=0.0001,
            previous_statement_value=0.00001,
            serial=1,
            explanation=fake.text(),
            present_statement_value=0.0002
        )
        return statement

    @staticmethod
    def create_contract_1():
        contract = Contract.objects.create(
            title='gas',
            code=1,
            amount=0.00001,
        )
        return contract

    @staticmethod
    def create_contract_2():
        contract = Contract.objects.create(
            title='gasoline',
            code=2,
            amount=0.00002,
        )
        return contract

    @property
    def data1(self):
        fake = Faker()
        cn = Contract.objects.get(code=1)
        return {
            "type": "n",
            "contract": cn.id,
            "value": 0.000001,
            "serial": 1,
            "explanation": fake.text()
        }

    @property
    def data2(self):
        fake = Faker()
        cn = Contract.objects.get(code=2)
        return {
            "type": "n",
            "contract": cn.id,
            "value": 0.0002,
            "serial": 2,
            "explanation": fake.text()
        }

    @property
    def data3(self):
        fake = Faker()
        return {
            "type": "n",
            "contract": 4,
            "value": 0.000003,
            "serial": 3,
            "explanation": fake.text()
        }

    def test_get_all_statement(self):
        client = APIClient()
        user = User.objects.all().first()
        self.client.force_authenticate(user)
        url = '/contracting/statement/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_statement(self):
        self.create_contract_1()
        self.create_contract_2()
        client = APIClient()
        user = User.objects.all().first()
        self.client.force_authenticate(user)
        response = self.client.post(reverse('statement'), data=self.data1, format='json')
        response1 = self.client.post(reverse('statement'), data=self.data2, format='json')
        response2 = self.client.post(reverse('statement'), data=self.data3, format='json')
        import decimal
        print(response.data)
        print(response1.data)
        print(response2.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['code'], 1)
        self.assertEqual(response1.data['code'], 1)
        self.assertEqual(response2.data['code'], response1.data['code']+1)

        self.assertEqual(decimal.Decimal(response2.data['present_statement_value']),
                         decimal.Decimal(response2.data['previous_statement_value'])
                         + decimal.Decimal(response2.data['value']))
        self.assertEqual(decimal.Decimal(response2.data['previous_statement_value']),
                         decimal.Decimal(response1.data['present_statement_value']))

    def test_delete_statement(self):
        self.create_statement()
        client = APIClient()
        user = User.objects.all().first()
        self.client.force_authenticate(user)
        url = '/contracting/statement/1/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SupplementTest(MTestCase):
    @staticmethod
    def create_supplement():
        fake = Faker()
        cn = Contract.objects.create(title='hybrid', code=1, amount=0.00001)
        supplement = Supplement.objects.create(
            contract=cn,
            explanation=fake.text(),
            value=0.0003,
            code=1
        )
        return supplement

    @staticmethod
    def create_contract():
        contract = Contract.objects.create(
            title='gas',
            code=5,
            max_change_amount=7,
            amount=0.00001,
        )
        return contract

    @property
    def data1(self):
        fake = Faker()
        con = Contract.objects.get(code=5).id
        return {
            "contract": con,
            "explanation": fake.text(),
            "value": 0.00001,
            "code": 2
        }

    @property
    def data2(self):
        fake = Faker()
        con = Contract.objects.get(code=5).id
        return {
            "contract": con,
            "explanation": fake.text(),
            "value": 0.00999,
            "code": 3
        }

    def test_get_all_supplement(self):
        client = APIClient()
        user = User.objects.all().first()
        self.client.force_authenticate(user)
        url = '/contracting/supplement/'
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_supplement(self):
        self.create_contract()
        client = APIClient()
        user = User.objects.all().first()
        self.client.force_authenticate(user)
        response = self.client.post(reverse('supplementApi'), data=self.data1, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_supplement(self):
        self.create_supplement()
        client = APIClient()
        user = User.objects.all().first()
        self.client.force_authenticate(user)
        url = '/contracting/supplement/2/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_amount_validate(self):
        self.create_contract()
        client = APIClient()
        user = User.objects.all().first()
        self.client.force_authenticate(user)
        response = self.client.post(reverse('supplementApi'), data=self.data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_contract_supplement(self):
        con = Contract.objects.create(title='test', code=10, max_change_amount=7, amount=0.00001)
        Supplement.objects.create(contract=con, explanation='blahblahblah',
                                  value=0.00001, code=3)

        client = APIClient()
        user = User.objects.all().first()
        self.client.force_authenticate(user)
        url = '/contracting/contract/10/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
