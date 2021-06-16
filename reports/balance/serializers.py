from rest_framework import serializers
from accounts.accounts.models import Account


class BalanceAccountSerializer(serializers.ModelSerializer):
    bed_sum = serializers.IntegerField()
    bes_sum = serializers.IntegerField()
    bed_remain = serializers.IntegerField()
    bes_remain = serializers.IntegerField()

    opening_bed_sum = serializers.IntegerField()
    opening_bes_sum = serializers.IntegerField()

    previous_bed_sum = serializers.IntegerField()
    previous_bes_sum = serializers.IntegerField()

    floatAccounts_data = serializers.ReadOnlyField()
    costCenters_data = serializers.ReadOnlyField()
    type_data = serializers.ReadOnlyField()

    class Meta:
        model = Account
        fields = ('id', 'code', 'name', 'level', 'bed_sum', 'bes_sum', 'bed_remain', 'bes_remain', 'opening_bed_sum',
                  'opening_bes_sum', 'previous_bed_sum', 'previous_bes_sum', 'floatAccounts_data', 'costCenters_data',
                  'type_data')
