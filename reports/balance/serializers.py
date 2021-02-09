from rest_framework import serializers
from accounts.accounts.models import Account


class BalanceAccountSerializer(serializers.ModelSerializer):
    bed_sum = serializers.IntegerField()
    bes_sum = serializers.IntegerField()
    bed_remain = serializers.IntegerField()
    bes_remain = serializers.IntegerField()

    floatAccounts_data = serializers.ReadOnlyField()
    costCenters_data = serializers.ReadOnlyField()
    type_data = serializers.ReadOnlyField()

    class Meta:
        model = Account
        fields = ('id', 'code', 'name', 'level', 'bed_sum', 'bes_sum', 'bed_remain', 'bes_remain',
                  'floatAccounts_data',
                  'costCenters_data',
                  'type_data')
