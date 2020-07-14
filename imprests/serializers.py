from typing import Any

from rest_framework import serializers

from accounts.accounts.serializers import AccountListRetrieveSerializer, FloatAccountSerializer
from imprests.models import ImprestSettlementItem, ImprestSettlement
from transactions.serializers import TransactionListRetrieveSerializer


class ImprestSettlementItemListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountListRetrieveSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    costCenter = FloatAccountSerializer(read_only=True, many=False)

    class Meta:
        model = ImprestSettlementItem
        fields = '__all__'


class ImprestSettlementItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImprestSettlementItem
        fields = '__all__'
        read_only_fields = ('financial_year',)


class ImprestSettlementCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImprestSettlement
        fields = '__all__'
        read_only_fields = ('financial_year', 'code')


class ImprestSettlementListRetrieveSerializer(serializers.ModelSerializer):
    items = ImprestSettlementItemListRetrieveSerializer(read_only=True, many=True)
    transaction = TransactionListRetrieveSerializer(read_only=True)

    class Meta:
        model = ImprestSettlement
        fields = '__all__'
