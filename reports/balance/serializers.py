from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework import serializers

from accounts.accounts.models import Account, FloatAccount, FloatAccountGroup


class BalanceFloatAccountSerializer(serializers.ModelSerializer):
    bed_sum = serializers.IntegerField()
    bes_sum = serializers.IntegerField()
    bed_remain = serializers.IntegerField()
    bes_remain = serializers.IntegerField()

    class Meta:
        model = FloatAccount
        fields = '__all__'


class BalanceFloatAccountGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = FloatAccountGroup
        fields = '__all__'


class BalanceAccountSerializer(serializers.ModelSerializer):
    bed_sum = serializers.IntegerField()
    bes_sum = serializers.IntegerField()
    bed_remain = serializers.IntegerField()
    bes_remain = serializers.IntegerField()

    _floatAccountGroup = serializers.ReadOnlyField()
    _floatAccounts = serializers.ReadOnlyField()
    _bank = serializers.ReadOnlyField()
    _person = serializers.ReadOnlyField()

    class Meta:
        model = Account
        fields = ('id', 'code', 'name', 'level', 'bed', 'bes', 'bed_sum', 'bes_sum', 'bed_remain', 'bes_remain',
                  '_floatAccountGroup',
                  '_bank',
                  '_person',
                  '_floatAccounts')

