from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from accounts.accounts.models import *


class FloatAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloatAccount
        fields = ('pk', 'name', 'explanation', 'max_bed', 'max_bes', 'max_bed_with_sanad', 'max_bes_with_sanad', 'floatAccountGroup')


class FloatAccountGroupSerializer(serializers.ModelSerializer):
    floatAccounts = FloatAccountSerializer(many=True, read_only=True)

    class Meta:
        model = FloatAccountGroup
        fields = ('pk', 'name', 'explanation', 'floatAccounts')


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = ('pk', 'name', 'type', 'explanation')


class AccountSerializer(serializers.ModelSerializer):
    children = serializers.ListSerializer(read_only=True, child=RecursiveField())
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.code + ' - ' + obj.name

    class Meta:
        model = Account
        fields = (
            'pk',
            'name',
            'code',
            'explanation',
            'is_disabled',
            'max_bed',
            'max_bes',
            'max_bed_with_sanad',
            'max_bes_with_sanad',
            'created_at',
            'updated_at',
            'level',
            'type',
            'costCenter',
            'parent',
            'title',
            'floatAccountGroup',
            'children',
        )

    def validate(self, data):
        CODE_LENGTHS = [1, 3, 5, 9]
        PARENT_PART = [0, 1, 3, 5]
        if len(data['code']) != CODE_LENGTHS[data['level']]:
            raise serializers.ValidationError("کد حساب نا معتبر می باشد")
        if data['level'] != 0:
            if 'parent' not in data.keys():
                raise serializers.ValidationError("حساب های زیر مجموعه گروه، باید پدر داشته باشند")
            if data['parent'].code != data['code'][0:PARENT_PART[data['level']]]:
                raise serializers.ValidationError("کد حساب، با حساب پدر مطابقت ندارد")
            if data['parent'].level != data['level'] - 1:
                raise serializers.ValidationError("سطح حساب، با حساب پدر مطابقت ندارد")
        else:
            if 'parent' in data.keys() and data['parent'] is not None:
                raise serializers.ValidationError("حساب گروه، نمی تواند پدر داشته باشد")

        if 'floatAccountGroup' in data.keys() and data['floatAccountGroup'] is not None and data['level'] != 3:
            raise serializers.ValidationError("تنها حساب سطح آخر (تفضیلی) می تواند دارای گروه حساب شناور باشد")

        if 'costCenter' in data.keys() and data['costCenter'] is not None and data['level'] != 3:
            raise serializers.ValidationError("تنها حساب سطح آخر (تفضیلی) می تواند دارای مرکز هزینه باشد")

        return data

    def create(self, validated_data):
        data = validated_data.copy()
        if data['level'] != 0 and ('type' not in data.keys() or ('type' in data.keys() and data['type'] is None)):
            data['type'] = data['parent'].type

        return Account.objects.create(**data)
        return super(AccountSerializer, self).create(**data)


class AccountListRetrieveSerializer(AccountSerializer):
    floatAccountGroup = FloatAccountGroupSerializer(read_only=True)
    type = AccountTypeSerializer(read_only=True)




