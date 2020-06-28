from typing import Type

from django.db.models.base import Model


def get_current_user():
    from helpers.middlewares.ModifyRequestMiddleware import ModifyRequestMiddleware

    return ModifyRequestMiddleware.user


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
        code = model.objects.inFinancialYear().latest('code').code + 1
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
