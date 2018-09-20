from rest_framework import serializers

from accounts.accounts.models import Account


class AccountBalanceSerializer(serializers.ModelSerializer):
    bed_sum = serializers.IntegerField()
    bes_sum = serializers.IntegerField()
    bed_remain = serializers.IntegerField()
    bes_remain = serializers.IntegerField()

    class Meta:
        model = Account
        fields = ('id', 'code', 'name', 'level', 'bed', 'bes', 'bed_sum', 'bes_sum', 'bed_remain', 'bes_remain')

