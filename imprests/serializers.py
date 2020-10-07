from rest_framework import serializers

from accounts.accounts.serializers import AccountRetrieveSerializer, FloatAccountSerializer, AccountListSerializer
from imprests.models import ImprestSettlementItem, ImprestSettlement
from sanads.serializers import SanadSerializer
from transactions.models import Transaction
from transactions.serializers import TransactionListRetrieveSerializer, TransactionItemListRetrieveSerializer
from users.serializers import UserSimpleSerializer


class ImprestSettlementItemListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountListSerializer(read_only=True, many=False)
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
    items = ImprestSettlementItemListRetrieveSerializer(read_only=True, many=True)

    class Meta:
        model = ImprestSettlement
        fields = '__all__'
        read_only_fields = ('financial_year', 'code')


class ImprestSettlementListRetrieveSerializer(serializers.ModelSerializer):
    items = ImprestSettlementItemListRetrieveSerializer(read_only=True, many=True)
    transaction = TransactionListRetrieveSerializer(read_only=True)
    sanad = SanadSerializer(read_only=True, many=False)
    created_by = UserSimpleSerializer(many=False, read_only=True)

    class Meta:
        model = ImprestSettlement
        fields = '__all__'


class ImprestListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountRetrieveSerializer(read_only=True, many=False)
    items = TransactionItemListRetrieveSerializer(read_only=True, many=True)
    sanad = SanadSerializer(read_only=True, many=False)
    imprestSettlements = ImprestSettlementCreateUpdateSerializer(many=True)

    class Meta:
        model = Transaction
        fields = '__all__'
