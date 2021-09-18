from rest_framework import serializers

from accounts.accounts.serializers import FloatAccountSerializer, AccountListSerializer
from accounts.accounts.validators import AccountValidator
from accounts.defaultAccounts.serializers import DefaultAccountListRetrieveSerializer
from cheques.serializers import ChequeRetrieveSerializer
from factors.models import Factor
from factors.models.factor import FactorPayment
from imprests.serializers import ImprestSettlementListRetrieveSerializer
from sanads.serializers import SanadSerializer
from transactions.models import *
from users.serializers import UserSimpleSerializer


class TransactionItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionItem
        fields = '__all__'
        read_only_fields = ('financial_year',)

    def validate(self, data):
        transaction_type = data['transaction'].type
        if transaction_type not in (Transaction.PAYMENT_GUARANTEE, Transaction.RECEIVED_GUARANTEE):
            AccountValidator.tafsili(data)
        return super(TransactionItemCreateUpdateSerializer, self).validate(data)


class TransactionItemListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountListSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    costCenter = FloatAccountSerializer(read_only=True, many=False)
    type = DefaultAccountListRetrieveSerializer(read_only=True, many=False)
    cheque = ChequeRetrieveSerializer(read_only=True, many=False)

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


class TransactionFactorPaymentFactorRetrieveSerializer(serializers.ModelSerializer):
    totalSum = serializers.CharField()

    class Meta:
        model = Factor
        fields = ('id', 'type', 'code', 'temporary_code', 'explanation', 'date', 'totalSum', 'paidValue')


class TransactionFactorPaymentRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorPayment
        fields = '__all__'


class TransactionFactorListSerializer(serializers.ModelSerializer):
    remain = serializers.SerializerMethodField()
    previous_paid_value = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()
    back_total_sum = serializers.SerializerMethodField()

    def get_back_total_sum(self, obj: Factor):
        if hasattr(obj, 'backFactor'):
            return obj.backFactor.total_sum
        else:
            return 0

    def get_remain(self, obj: Factor):
        return obj.total_sum - self.get_back_total_sum(obj) - obj.paidValue

    def get_previous_paid_value(self, obj: Factor):
        payment = obj.payments.filter(transaction_id=self.transaction_id).first()
        if payment:
            return obj.paidValue - payment.value
        else:
            return obj.paidValue

    def get_payment(self, obj: Factor):
        payment = obj.payments.filter(transaction_id=self.transaction_id).first()
        if payment:
            return TransactionFactorPaymentRetrieveSerializer(payment).data
        else:
            return {
                'factor': obj.id,
                'value': 0
            }

    @property
    def transaction_id(self):
        return self.context.get('transaction_id')

    class Meta:
        model = Factor
        fields = (
            'id', 'type', 'code', 'temporary_code', 'explanation', 'date', 'total_sum', 'remain', 'previous_paid_value',
            'payment',
            'back_total_sum'
        )


class TransactionListRetrieveSerializer(serializers.ModelSerializer):
    account = AccountListSerializer(read_only=True, many=False)
    floatAccount = FloatAccountSerializer(read_only=True, many=False)
    costCenter = FloatAccountSerializer(read_only=True, many=False)
    items = TransactionItemListRetrieveSerializer(read_only=True, many=True)
    sanad = SanadSerializer(read_only=True, many=False)
    imprestSettlement = ImprestSettlementListRetrieveSerializer(read_only=True, many=False)
    created_by = UserSimpleSerializer(many=False, read_only=True)
    factorPayments = TransactionFactorPaymentRetrieveSerializer(many=True)

    class Meta:
        model = Transaction
        fields = '__all__'


class BankingOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankingOperation
        fields = '__all__'
        read_only_fields = ('financial_year',)
