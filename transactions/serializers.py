from rest_framework import serializers

from accounts.accounts.serializers import AccountListRetrieveSerializer, FloatAccountSerializer
from accounts.accounts.validators import AccountValidator
from accounts.defaultAccounts.serializers import DefaultAccountListRetrieveSerializer
from cheques.serializers import ChequeListRetrieveSerializer
from transactions.models import *


class TransactionItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionItem
        fields = '__all__'
        read_only_fields = ('financial_year',)

    def validate(self, data):
        AccountValidator.tafsili(data)
        return super(TransactionItemCreateUpdateSerializer, self).validate(data)


class TransactionItemListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountListRetrieveSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    costCenter = FloatAccountSerializer(read_only=True, many=False)
    type = DefaultAccountListRetrieveSerializer(read_only=True, many=False)
    cheque = ChequeListRetrieveSerializer(read_only=True, many=False)

    class Meta:
        model = TransactionItem
        fields = '__all__'


class TransactionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('financial_year', 'code', 'sanad')

    def validate(self, data):
        AccountValidator.tafsili(data)
        return super(TransactionCreateUpdateSerializer, self).validate(data)


class TransactionListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountListRetrieveSerializer(read_only=True, many=False)
    items = TransactionItemListRetrieveSerializer(read_only=True, many=True)
    sanad_code = serializers.IntegerField(source="sanad.code")

    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionSerializerForPayment(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
