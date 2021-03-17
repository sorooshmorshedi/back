import functools
from decimal import Decimal
from typing import Type

import jdatetime
from django.db.models.base import Model
from django.db.models.query_utils import Q


def get_current_user():
    from helpers.middlewares.modify_request_middleware import ModifyRequestMiddleware
    return ModifyRequestMiddleware.thread_local.user


def get_new_child_code(parent_code, child_code_length, last_child_code=None):
    if last_child_code:
        last_code = int(last_child_code) + 1
        code = str(last_code)
    else:
        last_code = '1'.zfill(child_code_length)
        code = parent_code + last_code

    if code[:len(parent_code)] != parent_code:
        from rest_framework import serializers
        raise serializers.ValidationError("تعداد فرزندان این سطح پر شده است")

    return code


def get_new_code(model: Type[Model], max_length=None):
    try:
        code = model.objects.inFinancialYear().filter(~Q(code=None)).latest('code').code + 1
    except:
        return 1

    if max_length and len(str(code)) > max_length:
        from rest_framework import serializers
        raise serializers.ValidationError("تعداد اعضای این سطح پر شده است")

    return code


def get_object_by_code(queryset, position, object_id=None):
    try:
        item = None
        if position == 'next' and object_id:
            item = queryset.filter(pk__gt=object_id).order_by('id')[0]
        elif position == 'prev' and object_id:
            if object_id:
                queryset = queryset.filter(pk__lt=object_id)
            item = queryset.order_by('-id')[0]
        elif position == 'first':
            item = queryset.order_by('id')[0]
        elif position == 'last':
            item = queryset.order_by('-id')[0]
        return item
    except IndexError:
        return None


def float_to_str(f):
    float_string = repr(float(f))
    if 'e' in float_string:  # detect scientific notation
        digits, exp = float_string.split('e')
        digits = digits.replace('.', '').replace('-', '')
        exp = int(exp)
        zero_padding = '0' * (abs(int(exp)) - 1)  # minus 1 for decimal point in the sci notation
        sign = '-' if f < 0 else ''
        if exp > 0:
            float_string = '{}{}{}.0'.format(sign, digits, zero_padding)
        else:
            float_string = '{}0.{}{}'.format(sign, zero_padding, digits)
    return add_separator(float_string.strip('0').strip('.'))


def add_separator(value):
    if value is None:
        return ''
    elif value == 0:
        return 0
    try:
        str_value = '{:,}'.format(float(value))
    except ValueError:
        return value

    # str_value = str_value.replace(',', '/')

    if not str_value:
        str_value = '0'

    if str_value.endswith('.0'):
        str_value = str_value[:-2]

    return str_value


def get_object_accounts(obj):
    return {
        'account': obj.account,
        'floatAccount': obj.floatAccount,
        'costCenter': obj.costCenter
    }


def get_object_account_names(obj):
    arr = [obj.account.name]
    if obj.floatAccount: arr.append(obj.floatAccount.name)
    if obj.costCenter: arr.append(obj.costCenter.name)
    return " - ".join(arr)


def date_to_str(date: jdatetime.date):
    date = str(date).split('-')
    return '/'.join(date)


def sanad_exp(*args):
    result = ""
    for arg in args:
        if isinstance(arg, jdatetime.date):
            arg = date_to_str(arg)
        if isinstance(arg, Decimal):
            arg = str(arg).rstrip('0').rstrip('.')
        else:
            arg = str(arg)
        result += arg + " "

    return result[:-1]


def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        if isinstance(obj, dict):
            return obj.get(attr, None)
        else:
            if hasattr(obj, attr):
                return getattr(obj, attr, *args)
            else:
                return None

    return functools.reduce(_getattr, [obj] + attr.split('.'))


def to_gregorian(date):
    date = jdatetime.date(*list(map(int, date.split('-'))))
    return date.togregorian().isoformat()
