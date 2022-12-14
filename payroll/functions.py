
import json
from pprint import pprint
import re

import pandas as pd
from django.apps import apps
from django.core.exceptions import ValidationError
from django.core.management import CommandParser
from django.core.management.base import BaseCommand
from django.db.models import Q

from companies.models import FinancialYear
from distributions.models import Path
from factors.factor_sanad import FactorSanad
from factors.models import Factor
from helpers.test import set_user
from home.models import DefaultText
from server.settings import BASE_DIR
from users.models import User


class Command(BaseCommand):
    help = 'Load data from excel'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):

        file_path = options['file_path']
        data = pd.read_excel(file_path, sheet_name=None, skiprows=1)['Transformed by JSON-CSV.CO'].to_dict()

        user = User.objects.get(pk=data.pop('user')[0])
        set_user(user)

        financial_year = FinancialYear.objects.get(pk=data.pop('financial_year')[0])

        app_label = data.pop('app_label')[0]
        model_name = data.pop('model_name')[0]
        Model = apps.get_model(app_label, model_name)

        id_map = {}

        items_count = len(data['id'])
        fields = list(data.keys())
        fields.pop(0)
        for i in range(items_count):

            item_data = {}
            local_id = int(data['id'][i])
            for field in fields:
                value = data[field][i]

                # Check nan values
                if value != value:
                    value = None
                # Replace parent id with db id
                elif field == 'parent_id':
                    value = id_map[int(value)]

                item_data[field] = value

            item = Model.objects.create(
                financial_year=financial_year,
                **item_data
            )
            id_map[local_id] = item.id

        print(id_map)


def is_shenase_meli(input_code):
    status = True
    message = 'شناسه ملی تایید شد'
    code = str(input_code)
    if len(code) != 11:
        status = False
        message = "شناسه ملی باید یازده رقم باشد"
    if status:
        try:
            control_number = int(code[10])
            tens_digit_plus_two = int(code[9]) + 2
        except ValueError:
            status = False
            message = "شناسه ملی وارد شده صحیح نیست"
    if status:
        try:
            tens_coefficients = (29, 27, 23, 19, 17)
            numbers_sum = 0
            i = 0
            while i < 10:
                my_index = i % 5
                numbers_sum += (tens_digit_plus_two + int(code[i])) * tens_coefficients[my_index]
                i += 1
            numbers_sum = numbers_sum % 11
            if numbers_sum == 10:
                numbers_sum = 0
            if numbers_sum != control_number:
                status = False
                message = "شناسه ملی وارد شده صحیح نیست"
        except ValueError:
            status = False
            message = "شناسه ملی وارد شده صحیح نیست"
    return status, message

def is_valid_melli_code(value):
    if not re.search(r'^\d{10}$', value):
        is_valid = False
    else:
        check = int(value[9])
        s = sum([int(value[x]) * (10 - x) for x in range(9)]) % 11
        is_valid = (2 > s == check) or (s >= 2 and check + s == 11)
    return is_valid, "کد ملی وارد شده صحیح نیست"
