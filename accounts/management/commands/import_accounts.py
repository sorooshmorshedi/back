import json
from pprint import pprint

import pandas as pd
from django.apps import apps
from django.core.management import CommandParser
from django.core.management.base import BaseCommand
from pandas import DataFrame

from accounts.accounts.models import AccountType, Account
from companies.models import FinancialYear, Company
from helpers.test import set_user
from server.settings import BASE_DIR
from users.models import User


class Command(BaseCommand):
    help = 'Import Accounts from ./new-coding.xlsx'

    def handle(self, *args, **options):
        user = User.objects.get(pk=1)
        set_user(user)

        file_path = BASE_DIR + '/new-coding.xlsx'

        sheet_names = ['ادواری', 'دائمی']
        for sheet_name in sheet_names:
            print("Working on:")
            print("\t-\t", sheet_name)
            company_name = 'کدینگ پیشفرض {}'.format(sheet_name)

            data: DataFrame = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=0)
            data = data.to_dict()

            company, created = Company.objects.get_or_create(
                name=company_name,
                superuser=user,
            )
            financial_year, created = FinancialYear.objects.get_or_create(
                company=company,
                name=company_name,
                start='1399-01-01',
                end='1400-01-01'
            )

            objects_data = []
            for i in range(len(data['code'])):
                code = str(data['code'][i])
                name = data['name'][i]
                type_name = data['type'][i]
                account_type = AccountType.objects.filter(name=type_name).first()

                if not account_type:
                    print("Account type does not exists: {}:{}".format(i, type_name))
                    continue

                level = {1: 0, 3: 1, 5: 2, 9: 3}[len(code)]

                parent_code = None
                if level != 0:
                    parent_code = code[:{0: 1, 1: 3, 2: 5, 3: 9}[level - 1]]

                objects_data.append({
                    'parent_code': parent_code,
                    'financial_year': financial_year,
                    'code': code,
                    'name': name,
                    'type': account_type,
                    'level': level,
                    'account_type': Account.OTHER
                })

            objects_data.sort(key=lambda x: x['level'])

            for data in objects_data:
                parent_code = data.pop('parent_code')
                parent = None
                if parent_code:
                    try:
                        parent = Account.objects.get(financial_year=financial_year, code=parent_code)
                    except Account.DoesNotExist as e:
                        print(parent_code, "Does not exists")
                        continue
                account, created = Account.objects.get_or_create(**data, parent=parent)
