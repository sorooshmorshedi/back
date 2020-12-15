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

    floatAccountGroup_data = serializers.ReadOnlyField()
    floatAccounts_data = serializers.ReadOnlyField()
    costCenterGroup_data = serializers.ReadOnlyField()
    costCenters_data = serializers.ReadOnlyField()
    type_data = serializers.ReadOnlyField()

    class Meta:
        model = Account
        fields = ('id', 'code', 'name', 'level', 'bed_sum', 'bes_sum', 'bed_remain', 'bes_remain',
                  'floatAccountGroup_data',
                  'floatAccounts_data',
                  'costCenterGroup_data',
                  'costCenters_data',
                  'type_data')


class FloatBalanceSerializer(serializers.Serializer):
    bed_sum = serializers.IntegerField()
    bes_sum = serializers.IntegerField()
    bed_remain = serializers.IntegerField()
    bes_remain = serializers.IntegerField()

    group_name = serializers.CharField()
    float_account_name = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
