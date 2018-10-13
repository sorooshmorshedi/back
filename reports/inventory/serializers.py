from rest_framework import serializers

from accounts.accounts.models import Account
from accounts.accounts.serializers import AccountSerializer
from factors.models import FactorItem, Factor
from factors.serializers import FactorSerializer
from sanads.sanads.models import SanadItem, Sanad


class AccountInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'code', 'name')


class FactorWithAccountSerializer(FactorSerializer):
    account = AccountInventorySerializer(many=False, read_only=True)

    class Meta:
        model = Factor
        fields = ('id', 'code', 'date', 'type', 'isPaid', 'account')


class FactorItemInventorySerializer(serializers.ModelSerializer):
    factor = FactorWithAccountSerializer(many=False, read_only=True)
    input = serializers.DictField()
    output = serializers.DictField()
    remain = serializers.DictField()

    class Meta:
        model = FactorItem
        fields = ('id', 'input', 'output', 'remain', 'factor',)

